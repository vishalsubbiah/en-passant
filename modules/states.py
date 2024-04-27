"""Manages session states variables.
"""


import streamlit as st
from st_bridge import bridge
import datetime as dt


def init_states():
    if 'next' not in st.session_state:
        st.session_state.next = 0

    if ('curfen' not in st.session_state) or ('moves' not in st.session_state) :
        st.session_state.curside = 'white'
        st.session_state.curfen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        st.session_state.moves = {
            st.session_state.curfen : {
                    'side':'GAME START', 
                    'curfen':st.session_state.curfen,
                    'last_fen':'',
                    'last_move':'',
                    'data':None,
                    'timestamp':str(dt.datetime.now())
                    
                }
        }

    # Get the info from current board after the user made the move.
    # The data will return the move, fen and the pgn.
    # The move contains the from sq, to square, and others.
