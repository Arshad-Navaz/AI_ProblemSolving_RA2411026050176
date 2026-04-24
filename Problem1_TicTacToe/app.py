import streamlit as st
import math
import time

st.title("Tic-Tac-Toe AI")
st.write("Play against an AI using Minimax or Alpha-Beta Pruning")

# ── Initialize session state ──────────────────────────────────────────────────
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "current_turn" not in st.session_state:
    st.session_state.current_turn = "human"
if "mm_nodes" not in st.session_state:
    st.session_state.mm_nodes = 0
if "ab_nodes" not in st.session_state:
    st.session_state.ab_nodes = 0
if "mm_time" not in st.session_state:
    st.session_state.mm_time = 0.0
if "ab_time" not in st.session_state:
    st.session_state.ab_time = 0.0
if "move_log" not in st.session_state:
    st.session_state.move_log = []

# ── Sidebar settings ──────────────────────────────────────────────────────────
st.sidebar.header("Settings")
human_sym = st.sidebar.radio("You play as:", ["X", "O"])
ai_sym = "O" if human_sym == "X" else "X"
algo = st.sidebar.radio("AI Algorithm:", ["Minimax", "Alpha-Beta Pruning"])

if st.sidebar.button("New Game"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = "human"
    st.session_state.mm_nodes = 0
    st.session_state.ab_nodes = 0
    st.session_state.mm_time = 0.0
    st.session_state.ab_time = 0.0
    st.session_state.move_log = []
    st.rerun()

# ── Game Logic ────────────────────────────────────────────────────────────────
def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # cols
        (0,4,8), (2,4,6)             # diagonals
    ]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    return all(cell != "" for cell in board)

# Minimax (no pruning)
def minimax(board, is_maximizing, ai, human, counter):
    counter[0] += 1
    winner = check_winner(board)
    if winner == ai:     return 10
    if winner == human:  return -10
    if is_full(board):   return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = ai
                best = max(best, minimax(board, False, ai, human, counter))
                board[i] = ""
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = human
                best = min(best, minimax(board, True, ai, human, counter))
                board[i] = ""
        return best

def best_move_minimax(board, ai, human):
    counter = [0]
    start = time.perf_counter()
    best_val, best_idx = -math.inf, -1
    for i in range(9):
        if board[i] == "":
            board[i] = ai
            val = minimax(board, False, ai, human, counter)
            board[i] = ""
            if val > best_val:
                best_val, best_idx = val, i
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    return best_idx, counter[0], elapsed

# Alpha-Beta Pruning
def alpha_beta(board, is_maximizing, ai, human, alpha, beta, counter):
    counter[0] += 1
    winner = check_winner(board)
    if winner == ai:     return 10
    if winner == human:  return -10
    if is_full(board):   return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = ai
                best = max(best, alpha_beta(board, False, ai, human, alpha, beta, counter))
                board[i] = ""
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # prune
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = human
                best = min(best, alpha_beta(board, True, ai, human, alpha, beta, counter))
                board[i] = ""
                beta = min(beta, best)
                if beta <= alpha:
                    break  # prune
        return best

def best_move_alpha_beta(board, ai, human):
    counter = [0]
    start = time.perf_counter()
    best_val, best_idx = -math.inf, -1
    for i in range(9):
        if board[i] == "":
            board[i] = ai
            val = alpha_beta(board, False, ai, human, -math.inf, math.inf, counter)
            board[i] = ""
            if val > best_val:
                best_val, best_idx = val, i
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    return best_idx, counter[0], elapsed

# ── Display Board ─────────────────────────────────────────────────────────────
st.subheader("Game Board")
st.write("Click a button to make your move:")

board = st.session_state.board

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        cell = board[idx]
        label = cell if cell != "" else f"{idx+1}"
        with cols[col]:
            if not st.session_state.game_over and cell == "" and st.session_state.current_turn == "human":
                if st.button(label, key=f"cell_{idx}", use_container_width=True):
                    board[idx] = human_sym
                    st.session_state.move_log.append(f"You played cell {idx+1}")
                    winner = check_winner(board)
                    if winner:
                        st.session_state.game_over = True
                        st.session_state.winner = winner
                    elif is_full(board):
                        st.session_state.game_over = True
                        st.session_state.winner = "draw"
                    else:
                        st.session_state.current_turn = "ai"
                    st.rerun()
            else:
                st.button(label, key=f"cell_{idx}", disabled=True, use_container_width=True)

# ── AI Move ───────────────────────────────────────────────────────────────────
if not st.session_state.game_over and st.session_state.current_turn == "ai":
    if algo == "Minimax":
        idx, nodes, t = best_move_minimax(board, ai_sym, human_sym)
        st.session_state.mm_nodes = nodes
        st.session_state.mm_time = t
        st.session_state.move_log.append(f"AI (Minimax) played cell {idx+1} | nodes={nodes} | time={t}ms")
    else:
        idx, nodes, t = best_move_alpha_beta(board, ai_sym, human_sym)
        st.session_state.ab_nodes = nodes
        st.session_state.ab_time = t
        st.session_state.move_log.append(f"AI (Alpha-Beta) played cell {idx+1} | nodes={nodes} | time={t}ms")

    if idx != -1:
        board[idx] = ai_sym

    winner = check_winner(board)
    if winner:
        st.session_state.game_over = True
        st.session_state.winner = winner
    elif is_full(board):
        st.session_state.game_over = True
        st.session_state.winner = "draw"
    else:
        st.session_state.current_turn = "human"
    st.rerun()

# ── Game Status ───────────────────────────────────────────────────────────────
st.subheader("Status")
if st.session_state.game_over:
    if st.session_state.winner == "draw":
        st.info("It's a DRAW! Perfect play from both sides.")
    elif st.session_state.winner == human_sym:
        st.success(f"You WIN! (played as {human_sym})")
    else:
        st.error(f"AI WINS! (played as {ai_sym})")
    st.write("Click 'New Game' in the sidebar to play again.")
else:
    if st.session_state.current_turn == "human":
        st.info(f"Your turn — you are '{human_sym}', click any numbered cell above")
    else:
        st.warning("AI is thinking...")

# ── Performance Comparison ────────────────────────────────────────────────────
st.subheader("Algorithm Performance Comparison")

col1, col2 = st.columns(2)

with col1:
    st.write("**Minimax**")
    st.metric("Nodes Explored", st.session_state.mm_nodes)
    st.metric("Execution Time (ms)", st.session_state.mm_time)
    st.write("Explores ALL possible game states. Slow but complete.")

with col2:
    st.write("**Alpha-Beta Pruning**")
    st.metric("Nodes Explored", st.session_state.ab_nodes)
    st.metric("Execution Time (ms)", st.session_state.ab_time)
    st.write("Skips branches that won't affect result. Faster than Minimax.")

if st.session_state.mm_nodes > 0 and st.session_state.ab_nodes > 0:
    reduction = round((1 - st.session_state.ab_nodes / st.session_state.mm_nodes) * 100, 1)
    st.success(f"Alpha-Beta pruned {reduction}% of nodes compared to Minimax!")

st.caption("Note: Switch algorithm in sidebar and replay to compare both.")

# ── Move Log ──────────────────────────────────────────────────────────────────
if st.session_state.move_log:
    st.subheader("Move Log")
    for entry in st.session_state.move_log:
        st.text(entry)
