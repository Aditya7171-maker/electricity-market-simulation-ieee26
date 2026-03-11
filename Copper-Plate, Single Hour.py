import pyomo.environ as pe
import pyomo.opt as po
import matplotlib.pyplot as plt
import pandas as pd
# -----------------------
# SOLVER
# This selects GLPK, a linear programming solver.
solver = po.SolverFactory('glpk')

# -----------------------
# MODEL
# ConcreteModel() - creates the optimization model
#Suffix - allows you to extract dual variables
model = pe.ConcreteModel()
model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)
# -----------------------
# SETS
# This defines 13 generators in the system.
model.G = pe.Set(initialize=[
    'U1','U2','U3','U4','U5','U6','U7','U8',
    'U9','U10','U11','U12','Wind'
])

# -----------------------
# PARAMETERS
# -----------------------

# Marginal costs ($/MWh) — use RTS data
gen_cost = {
    'U1': 13.32,
    'U2': 13.32,
    'U3': 20.7,
    'U4': 20.93,
    'U5': 26.11,
    'U6': 10.52,
    'U7': 10.52,
    'U8': 6.02,
    'U9': 5.47,
    'U10': 0,
    'U11': 10.52,
    'U12': 10.89,
    'Wind': 0
}

# Generator capacities (MW)
gen_cap = {
    'U1': 152,
    'U2': 152,
    'U3': 350,
    'U4': 591,
    'U5': 60,
    'U6': 155,
    'U7': 155,
    'U8': 400,
    'U9': 400,
    'U10': 300,
    'U11': 310,
    'U12': 350,
    'Wind': 1200 * 0.4   # 40% availability
}

# Load for Hour 18
Demand = 2650.5

model.C = pe.Param(model.G, initialize=gen_cost)
model.Pmax = pe.Param(model.G, initialize=gen_cap)

# -----------------------
# VARIABLES
#This represents how much each generator produces.
model.g = pe.Var(model.G, domain=pe.NonNegativeReals)

# -----------------------
# OBJECTIVE (Min Cost)
#The solver tries to meet demand using the cheapest generators first.
def cost_rule(m):
    return sum(m.C[i] * m.g[i] for i in m.G)

model.obj = pe.Objective(rule=cost_rule, sense=pe.minimize)

# -----------------------
# CONSTRAINTS
# -----------------------

# Power balance - Total generation must equal system load.
def balance_rule(m):
    return sum(m.g[i] for i in m.G) == Demand

model.balance = pe.Constraint(rule=balance_rule)

# Generator limits - A generator cannot exceed its capacity.
def gen_limit_rule(m, i):
    return m.g[i] <= m.Pmax[i]

model.gen_limit = pe.Constraint(model.G, rule=gen_limit_rule)

# -----------------------
# SOLVE
# This runs the optimization and finds the lowest cost dispatch.
solver.solve(model)

# -----------------------
# RESULTS
# -----------------------

print("\nDispatch Results")
for i in model.G:
    print(i, round(model.g[i].value,2))

print("\nTotal Generation Cost =",
      round(pe.value(model.obj),2))

print("Market Clearing Price =",
      round(model.dual[model.balance], 2))

MCP = model.dual[model.balance]

print("\nProducer Profits")
for i in model.G:
    dispatch = model.g[i].value
    cost = model.C[i]
    profit = (MCP - cost) * dispatch
    print(i, round(profit,2))

bid_price = 100

consumer_surplus = (bid_price - MCP) * Demand
print("\nConsumer Surplus =", round(consumer_surplus,2))    


total_profit = sum((MCP - model.C[i]) *
                   model.g[i].value for i in model.G)

social_welfare = consumer_surplus + total_profit
print("\nSocial Welfare =", round(social_welfare,2))

total_WTP = 100 * 2650.5
total_cost = pe.value(model.obj)

print("Social Welfare =",
      round(total_WTP - total_cost,2))

results = pd.DataFrame({
    "Generator": list(model.G),
    "Dispatch(MW)": [model.g[i].value for i in model.G],
    "MarginalCost": [model.C[i] for i in model.G]
})

print(results)

gens = list(model.G)
dispatch = [model.g[i].value for i in model.G]

plt.bar(gens, dispatch)
plt.xticks(rotation=90)
plt.ylabel("Generation (MW)")
plt.title("Generator Dispatch - Hour 18")
plt.show()
df = pd.DataFrame({
    "Generator": list(model.G),
    "Cost": [model.C[i] for i in model.G],
    "Capacity": [model.Pmax[i] for i in model.G]
})

df = df.sort_values("Cost")

plt.step(df["Cost"], df["Capacity"].cumsum())
plt.xlabel("Marginal Cost ($/MWh)")
plt.ylabel("Cumulative Capacity (MW)")
plt.title("Merit Order Curve")
plt.show()

# Extract data
generators = list(model.G)
costs = [model.C[i] for i in generators]
dispatch = [model.g[i].value for i in generators]

MCP = model.dual[model.balance]

# Plot
plt.figure(figsize=(8,6))

plt.scatter(costs, dispatch)

# Label points with generator names
for i, gen in enumerate(generators):
    plt.text(costs[i], dispatch[i], gen)

# Market clearing price line
plt.axvline(x=MCP, linestyle='--')

plt.xlabel("Marginal Cost ($/MWh)")
plt.ylabel("Dispatch (MW)")
plt.title("Generator Marginal Cost vs Dispatch")

plt.grid(True)

plt.show()