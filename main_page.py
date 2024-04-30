from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import chess
import streamlit_scrollable_textbox as stx

from chat_script import ChatApp
from eleven_labs import ElevenVoice
from st_bridge import bridge
from modules.chess import Chess
from modules.utility import set_page
from modules.states import init_states

from guardrails.hub import NSFWText
from guardrails import Guard

import os
import datetime as dt


set_page(title='Chess', page_icon="♟️")
init_states()
if "chat_app" not in st.session_state:
    st.session_state.prev_data = ""
    st.session_state.chat_app = ChatApp(client="groq", model="llama3-8b-8192")
    st.session_state.eleven_voice = ElevenVoice()
    st.session_state.guard = Guard().use(NSFWText, threshold=0.8, validation_method="sentence", on_fail="exception")
    st.session_state.board_width = 500

# Get the info from current board after the user made the move.
# The data will return the move, fen and the pgn.
# The move contains the from sq, to square, and others.
data = bridge("my-bridge")
if not st.session_state.get('current_player') or st.session_state['current_player'] == 'Player 2':
    st.session_state['current_player'] = 'Player 1'
else:
    st.session_state['current_player'] = 'Player 2'
error = ""
print("default", f"{data=}", f"{st.session_state.prev_data=}")
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
    pgn_entry = data["pgn"]

    if st.session_state.prev_data != data["pgn"]:
        print("before update",  f"{data=}", f"{st.session_state.prev_data=}")
        st.session_state.prev_data = data["pgn"]
        print("inside if should match", f"{data=}", f"{st.session_state.prev_data=}")
        message, persona, output = st.session_state.chat_app.chat(pgn_entry)

        try:
            st.session_state.guard.validate(output)
        except Exception as e:
            error = str(e)
            print(e)
            
        if persona=="Gordon Ramsey":
            voice_id = os.environ["GORDON_VOICE_ID"]
        elif persona=="Aziz Ansari":
            voice_id = os.environ["AZIZ_VOICE_ID"]
        st.session_state.eleven_voice.generate_and_play_audio(output, voice_id)

if st.button('start new game'):
    print("pressing start new game")
    puzzle = None
    data = None
    init_states()

cols = st.columns([1, 1])

with cols[0]:
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

with cols[1]:
    st.markdown(
        """
        <div style="margin-top: 7.5px;">  <!-- Adjust the top margin as needed -->
            <img src="https://github.com/vishalsubbiah/pearvc_hackathon_chess_commentry/blob/vishal/integ_lichess/images.jpeg?raw=true" alt="Gordon" style="width:100%">  <!-- Ensure the image path is correct -->
        </div>
        """,
        unsafe_allow_html=True
    )

    # Apply the custom CSS class to the scrollable textbox container
    st.markdown(
        '<div class="scrollable-textbox-top-margin">',
        unsafe_allow_html=True
    )
    with st.container():
        records = ["MOVES\n--------------------------------"]
        records.append(error)
        # html( "<p>" + '\n\n'.join(records) + "</p>", scrolling=True)
        for key, value in list(st.session_state['moves'].items())[1:]:
            records.append( ('Player 1' if value['current_player'] == 'Player 2'else 'Player 2') + ' played ' + value['last_move'][-2:])
        stx.scrollableTextbox('\n\n'.join(records), height = 500, border=True)