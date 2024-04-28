# import streamlit as st

# st.set_page_config(layout='wide')

# # Adjust the size of the containers to have matching margin
# st.markdown(
#     """
#     <style>
#         .video-container {
#             background-color: white;
#             box-sizing: border-box;
#             margin-bottom: 32px; /* Adjust this value as needed */
#             height: calc(50vh - 10px); /* Adjusting the height to account for the margin */
#         }
#         .video-container2 {
#             background-color: white;
#             box-sizing: border-box;
#             height: calc(30.5vh - 10px); /* Adjusting the height to account for the margin */
#         }
#         .stImage {
#             margin: 0px !important;
#             padding: 0px !important;
#         }
#         /* Remove default Streamlit padding around the columns */
#         .block-container .row .col {
#             padding: 0px !important;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )

# # Main content with adjusted columns, using "medium" for a standard gap size
# col1, col2 = st.columns([2.2, 2], gap='medium')

# with col1:
#     st.image('./chessboard_image.png', use_column_width=True)

# with col2:
#     # Create two white containers to represent the video placeholders
#     st.markdown('<div class="video-container"></div>', unsafe_allow_html=True)
#     st.markdown('<div class="video-container2"></div>', unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import chess
import streamlit_scrollable_textbox as stx


from st_bridge import bridge
from modules.chess import Chess
from modules.utility import set_page
from modules.states import init_states

import datetime as dt

set_page(title='Chess', page_icon="♟️")
init_states()
st.session_state.board_width = 500

# Get the info from current board after the user made the move.
# The data will return the move, fen and the pgn.
# The move contains the from sq, to square, and others.
data = bridge("my-bridge")

if not st.session_state.get('current_player') or st.session_state['current_player'] == 'Player 2':
    st.session_state['current_player'] = 'Player 1'
else:
    st.session_state['current_player'] = 'Player 2'

if st.button('start new game'):
    puzzle = None
    data = None

if data is not None:
    st.session_state.lastfen = st.session_state.curfen
    st.session_state.curfen = data['fen']
    st.session_state.curside = data['move']['color'].replace('w','white').replace('b','black')
    st.session_state.moves.update(
        {
            st.session_state.curfen : {
                'side':st.session_state.curside, 
                'curfen':st.session_state.curfen,
                'last_fen':st.session_state.lastfen,
                'last_move':data['pgn'],
                'data': None,
                'timestamp': str(dt.datetime.now()),
                "current_player": st.session_state.current_player
            }
        }
    )


cols = st.columns([1, 2.5, 2])


with cols[1]:
    puzzle = Chess(st.session_state.board_width, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    components.html(
        puzzle.puzzle_board(),
        height=st.session_state.board_width + 75,
        scrolling=False
    )
    board = chess.Board(st.session_state.curfen)
    outcome = board.outcome()
    # st.warning(f'is_check: {board.is_check()}')
    # st.warning(f'is_checkmate: {board.is_checkmate()}')
    # st.warning(f'is_stalemate: {board.is_stalemate()}')
    # st.warning(f'is_insufficient_material: {board.is_insufficient_material()}')
    # if outcome:
    #     st.warning(f"Winner: { {True:'White',False:'Black'}.get(outcome.winner) }")

with cols[2]:
    st.markdown(
        """
        <div style="margin-top: 7.5px;">  <!-- Adjust the top margin as needed -->
            <img src="https://i.ibb.co/6Dh2QV4/gordon.png" alt="Gordon" style="width:100%">  <!-- Ensure the image path is correct -->
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Apply the custom CSS class to the scrollable textbox container
    st.markdown(
        '<div class="scrollable-textbox-top-margin">', 
        unsafe_allow_html=True
    )
    records = ['MOVES\n------------------------------------------']
    for key, value in list(st.session_state['moves'].items())[1:]:
        records.append( ('Plyaer 1' if value['current_player'] == 'Player 2'else 'Player 2') + ' played ' + value['last_move'][-2:])
    stx.scrollableTextbox('\n\n'.join(records), height=251, border=True)
    st.markdown('</div>', unsafe_allow_html=True)