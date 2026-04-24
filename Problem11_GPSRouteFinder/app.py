import streamlit as st
import heapq
import time

st.title("GPS City Route Finder")
st.write("Find the shortest path between cities using the A* Search Algorithm")

# ── A* Algorithm ──────────────────────────────────────────────────────────────
def astar(graph, heuristic, start, goal):
    """
    A* Search Algorithm
    f(n) = g(n) + h(n)
    g(n) = actual cost from start to n
    h(n) = heuristic estimate from n to goal
    """
    # Priority queue: (f_cost, g_cost, current_node, path)
    open_set = []
    heapq.heappush(open_set, (heuristic.get(start, 0), 0, start, [start]))

    visited = set()
    explored_order = []

    while open_set:
        f, g, node, path = heapq.heappop(open_set)

        if node in visited:
            continue

        visited.add(node)
        explored_order.append(node)

        # Goal reached
        if node == goal:
            return path, g, explored_order

        # Expand neighbors
        for neighbor, cost in graph.get(node, {}).items():
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic.get(neighbor, 0)
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float("inf"), explored_order


# ── Sidebar: Preset Graphs ────────────────────────────────────────────────────
st.sidebar.header("Settings")

preset_choice = st.sidebar.selectbox("Load a preset graph:", [
    "Assignment Example (A to F)",
    "Indian Cities",
    "Custom (add manually)"
])

# ── Initialize session state ──────────────────────────────────────────────────
if "graph" not in st.session_state:
    st.session_state.graph = {}
if "heuristic" not in st.session_state:
    st.session_state.heuristic = {}
if "result" not in st.session_state:
    st.session_state.result = None

# ── Load Presets ──────────────────────────────────────────────────────────────
if st.sidebar.button("Load Preset"):
    if preset_choice == "Assignment Example (A to F)":
        st.session_state.graph = {
            "A": {"B": 1, "C": 4},
            "B": {"A": 1, "D": 2, "E": 5},
            "C": {"A": 4, "D": 1},
            "D": {"B": 2, "C": 1, "F": 3},
            "E": {"B": 5, "F": 1},
            "F": {}
        }
        st.session_state.heuristic = {
            "A": 7, "B": 6, "C": 4, "D": 2, "E": 1, "F": 0
        }
    elif preset_choice == "Indian Cities":
        st.session_state.graph = {
            "Mumbai":     {"Pune": 150, "Surat": 280, "Nashik": 170},
            "Pune":       {"Mumbai": 150, "Hyderabad": 560},
            "Surat":      {"Mumbai": 280, "Ahmedabad": 265},
            "Nashik":     {"Mumbai": 170, "Aurangabad": 100},
            "Ahmedabad":  {"Surat": 265, "Delhi": 940},
            "Hyderabad":  {"Pune": 560, "Bengaluru": 570, "Chennai": 630},
            "Aurangabad": {"Nashik": 100, "Hyderabad": 470},
            "Bengaluru":  {"Hyderabad": 570, "Chennai": 350},
            "Chennai":    {"Bengaluru": 350, "Hyderabad": 630},
            "Delhi":      {"Ahmedabad": 940}
        }
        st.session_state.heuristic = {
            "Mumbai": 1400, "Pune": 1350, "Surat": 1200, "Nashik": 1300,
            "Ahmedabad": 950, "Hyderabad": 700, "Aurangabad": 1100,
            "Bengaluru": 350, "Chennai": 0, "Delhi": 2100
        }
    st.session_state.result = None
    st.rerun()

if st.sidebar.button("Clear Graph"):
    st.session_state.graph = {}
    st.session_state.heuristic = {}
    st.session_state.result = None
    st.rerun()

# ── Add Edge Manually ─────────────────────────────────────────────────────────
st.subheader("Add a Road (Edge)")
st.write("Enter two cities, the travel cost between them, and their heuristic values:")

col1, col2, col3 = st.columns(3)
with col1:
    src = st.text_input("From City", placeholder="e.g. A").strip().upper()
with col2:
    dst = st.text_input("To City", placeholder="e.g. B").strip().upper()
with col3:
    cost = st.number_input("Travel Cost", min_value=1, value=1)

col4, col5 = st.columns(2)
with col4:
    h_src = st.number_input("Heuristic h(From)", min_value=0, value=0)
with col5:
    h_dst = st.number_input("Heuristic h(To)", min_value=0, value=0)

if st.button("Add Road"):
    if src and dst and src != dst:
        if src not in st.session_state.graph:
            st.session_state.graph[src] = {}
        if dst not in st.session_state.graph:
            st.session_state.graph[dst] = {}
        st.session_state.graph[src][dst] = cost
        st.session_state.graph[dst][src] = cost
        st.session_state.heuristic[src] = h_src
        st.session_state.heuristic[dst] = h_dst
        st.session_state.result = None
        st.success(f"Added road: {src} <-> {dst} with cost {cost}")
    else:
        st.error("Please enter two different city names.")

# ── Display Current Graph ─────────────────────────────────────────────────────
if st.session_state.graph:
    st.subheader("Current City Graph")
    for city, neighbors in sorted(st.session_state.graph.items()):
        h_val = st.session_state.heuristic.get(city, 0)
        connections = ", ".join(f"{nb} (cost {c})" for nb, c in sorted(neighbors.items()))
        st.text(f"  {city} [h={h_val}]  -->  {connections if connections else 'No connections'}")

# ── Run A* ────────────────────────────────────────────────────────────────────
st.subheader("Find Shortest Route")

nodes = sorted(st.session_state.graph.keys())

if len(nodes) >= 2:
    col1, col2 = st.columns(2)
    with col1:
        start_node = st.selectbox("Start City", nodes)
    with col2:
        goal_node = st.selectbox("Goal City", nodes, index=min(1, len(nodes)-1))

    if st.button("Run A* Search"):
        start_time = time.perf_counter()
        path, total_cost, explored = astar(
            st.session_state.graph,
            st.session_state.heuristic,
            start_node,
            goal_node
        )
        elapsed = round((time.perf_counter() - start_time) * 1000, 4)

        st.session_state.result = {
            "path": path,
            "cost": total_cost,
            "explored": explored,
            "time": elapsed,
            "start": start_node,
            "goal": goal_node
        }
        st.rerun()
else:
    st.info("Load a preset or add at least 2 cities to find a route.")

# ── Show Results ──────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result
    st.subheader("A* Search Results")

    if res["path"] is None:
        st.error(f"No path found from {res['start']} to {res['goal']}.")
    else:
        path = res["path"]
        total_cost = res["cost"]
        explored = res["explored"]

        # Optimal path
        st.write("**Optimal Path Found:**")
        path_str = " --> ".join(path)
        st.success(f"{path_str}")

        # Step by step cost breakdown
        st.write("**Step-by-step cost breakdown:**")
        graph = st.session_state.graph
        cumulative = 0
        for i in range(len(path) - 1):
            edge_cost = graph.get(path[i], {}).get(path[i+1], 0)
            cumulative += edge_cost
            st.text(f"  {path[i]} --> {path[i+1]}  |  edge cost = {edge_cost}  |  cumulative = {cumulative}")

        st.write("")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cost", total_cost)
        with col2:
            st.metric("Path Length (nodes)", len(path))
        with col3:
            st.metric("Nodes Explored", len(explored))

        st.metric("Execution Time (ms)", res["time"])

        # Explored nodes
        st.write("**Nodes explored during search (in order):**")
        st.text("  " + " --> ".join(explored))

        # Which nodes were skipped
        skipped = [n for n in explored if n not in path]
        if skipped:
            st.write("**Nodes explored but NOT on optimal path (pruned by heuristic):**")
            st.text("  " + ", ".join(skipped))

        # Heuristic values used
        st.write("**Heuristic values h(n) used:**")
        h_table = {"City": [], "h(n) value": [], "On Path": []}
        for city in sorted(st.session_state.heuristic.keys()):
            h_table["City"].append(city)
            h_table["h(n) value"].append(st.session_state.heuristic[city])
            h_table["On Path"].append("Yes" if city in path else "No")
        st.table(h_table)

# ── Algorithm Explanation ─────────────────────────────────────────────────────
st.subheader("How A* Works")
st.write("""
A* is an informed search algorithm that finds the shortest path in a weighted graph.

**Formula:**  f(n) = g(n) + h(n)

- **g(n)** = actual cost from the start node to node n
- **h(n)** = heuristic estimate of cost from node n to the goal
- **f(n)** = total estimated cost — used to decide which node to explore next

**How it works step by step:**
1. Start at the source node, add it to the open set (priority queue)
2. Always pick the node with the lowest f(n) from the open set
3. If that node is the goal, return the path
4. Otherwise, expand its neighbors and add them to the open set
5. Repeat until goal is found or open set is empty

**Why A* is better than BFS/DFS:**
- BFS explores in all directions equally (no guidance)
- DFS can go down wrong paths deeply
- A* uses the heuristic to guide search towards the goal — explores fewer nodes
- A* guarantees the optimal path when h(n) never overestimates the true cost (admissible heuristic)
""")
