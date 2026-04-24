# AI Problem Solving — GitHub Submission

> **Course:** Artificial Intelligence | **Team Size:** 2 members  
> **Implemented Problems:** Problem 1 (Tic-Tac-Toe AI) · Problem 11 (GPS Route Finder)  
> **Language:** Python 3 | **Framework:** Streamlit

---

## 🔗 Live Demos

| Problem | Live Link |
|---|---|
| Problem 1 — Tic-Tac-Toe AI | *(Add Streamlit Cloud URL after deploy)* |
| Problem 11 — GPS Route Finder | *(Add Streamlit Cloud URL after deploy)* |

---

## 📁 Repository Structure

```
AI_ProblemSolving/
├── Problem1_TicTacToe/
│   ├── app.py               # Main Streamlit app
│   ├── requirements.txt
│   └── README_P1.md
├── Problem11_GPSRouteFinder/
│   ├── app.py               # Main Streamlit app
│   ├── requirements.txt
│   └── README_P11.md
└── README.md                ← You are here
```

---

## Problem 1 — Interactive Game AI (Tic-Tac-Toe System)

### Case Study
A gaming company wants to create an AI opponent for a web-based Tic-Tac-Toe game. The AI always makes the optimal move. This implementation compares two algorithms — **Minimax** and **Alpha-Beta Pruning** — in real time.

### Algorithms Used

#### Minimax Algorithm
- Recursively explores **all possible game states** to find the optimal move
- Time complexity: **O(b^d)** where b = branching factor, d = depth
- Guarantees optimal play but explores every node — slower

#### Alpha-Beta Pruning
- Enhancement of Minimax that **prunes branches** that cannot affect the final decision
- Maintains two bounds: **α** (best for maximizer) and **β** (best for minimizer)
- If `β ≤ α`, the branch is pruned (no further exploration needed)
- Time complexity: **O(b^(d/2))** in best case — **up to 50–70% fewer nodes explored**
- Still guarantees the same optimal result as pure Minimax

### How to Run Locally

```bash
cd Problem1_TicTacToe
pip install -r requirements.txt
streamlit run app.py
```

### Sample Output

```
User plays: X | AI plays: O
Algorithm: Alpha-Beta Pruning

Move 1 (AI): Cell 5 (center)
  → Nodes explored: 59 | Time: 0.8ms

Move 3 (AI): Cell 1 (corner)
  → Nodes explored: 12 | Time: 0.2ms

Result: DRAW (optimal play from both sides)

--- Performance Comparison ---
Alpha-Beta: 71 nodes  | 1.0ms total
Minimax:   255 nodes  | 3.4ms total
Pruning gain: 72.2%
```

### Features
- Choose to play as X or O
- Toggle between Minimax and Alpha-Beta in the same game
- Real-time node count and execution time display
- Winning cells highlighted
- Full move log

---

## Problem 11 — GPS-Based City Route Finder (A\* Algorithm)

### Case Study
A navigation system finds the fastest route between two city locations using an **informed search strategy**. The city is modeled as a weighted graph. The system uses the A\* algorithm with a heuristic to avoid exploring unnecessary nodes.

### Algorithm Used

#### A\* Search
- Informed search algorithm that combines **actual cost g(n)** and **heuristic estimate h(n)**
- **f(n) = g(n) + h(n)**
  - `g(n)` = cost from start to node n
  - `h(n)` = estimated (heuristic) cost from n to goal
  - `f(n)` = priority used in the min-heap open set
- Uses a **priority queue (min-heap)** — always expands the lowest f(n) node
- Guarantees optimal path when h(n) is **admissible** (never overestimates actual cost)
- **More efficient** than BFS/DFS/UCS for large graphs with good heuristics

### How to Run Locally

```bash
cd Problem11_GPSRouteFinder
pip install -r requirements.txt
streamlit run app.py
```

### Sample Input (Assignment Example)

```
Graph:
  A → B (1), C (4)
  B → D (2), E (5)
  C → D (1)
  D → F (3)
  E → F (1)

Heuristic h(n) to goal F:
  A:7, B:6, C:4, D:2, E:1, F:0

Start: A  |  Goal: F
```

### Sample Output

```
A* Search Result:
  Optimal Path: A → B → D → F
  Total Cost:   1 + 2 + 3 = 6

  Nodes Explored (order): A, B, C, D, F
  Nodes on path:  A, B, D, F
  Nodes pruned:   C, E

  Execution time: 0.04ms
```

### Features
- Preloaded graphs: Assignment example + Indian Cities network
- Dynamically add nodes and edges through the UI
- Color-coded path visualization (blue = on path, red = explored but pruned)
- Heuristic table displayed alongside results
- Handles disconnected graphs (no path found message)

---

## Execution Steps (Both Problems)

### Option A — Run Locally
```bash
git clone https://github.com/<your-username>/AI_ProblemSolving_<RegisterNumber>
cd AI_ProblemSolving_<RegisterNumber>

# Problem 1
cd Problem1_TicTacToe && pip install -r requirements.txt && streamlit run app.py

# Problem 11
cd ../Problem11_GPSRouteFinder && pip install -r requirements.txt && streamlit run app.py
```

### Option B — Streamlit Cloud (Live Website)
1. Push this repository to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select this repo
4. Set **Main file path** to `Problem1_TicTacToe/app.py` (or Problem 11)
5. Click **Deploy**

---

## Comparison Summary

| Feature | Minimax | Alpha-Beta | A* |
|---|---|---|---|
| Problem Type | Game AI | Game AI | Pathfinding |
| Completeness | ✅ Always finds optimal | ✅ Same as Minimax | ✅ Optimal if h admissible |
| Nodes Explored | All (b^d) | Pruned (b^(d/2)) | Guided by heuristic |
| Speed | Slower | **Faster (50–70% less work)** | **Fastest for large graphs** |

---

## Team Members

| Name | Register Number |
|---|---|
| Member 1 | *(your reg number)* |
| Member 2 | *(partner reg number)* |

---

*Submitted for AI Problem Solving Assignment — April 2026*
## Team Project - AI Problem Solving
