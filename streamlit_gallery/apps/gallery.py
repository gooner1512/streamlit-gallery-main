import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.figure_factory as ff
from datetime import datetime
import datetime
from pathlib import Path


def main():    
    
    st.write('# :closed_book: Streamlit Components')
    st.markdown((Path(__file__).parents[2]/"README.md").read_text())
    st.markdown('Streamlit is **_really_ cool**.')
    st.markdown('This text is :red[colored red], and this is **:blue[colored]** and bold.')
    st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")

    st.title('This is a title')
    st.title('A title with _italics_ :blue[colors] and emojis :sunglasses:')

    st.header('This is a header')
    st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')

    st.subheader('This is a subheader')
    st.subheader('A subheader with _italics_ :blue[colors] and emojis :sunglasses:')

    st.caption('This is a string that explains something above.')
    st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')

    code = '''def hello():
        print("Hello, Streamlit!")'''
    st.code(code, language='python')

    st.text('This is some text.')

    st.latex(r'''
        a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
        \sum_{k=0}^{n-1} ar^k =
        a \left(\frac{1-r^{n}}{1-r}\right)
        ''')

    result = st.button("Click here")
    if result:
        st.write('Why click')
    else:
        st.write('Goodbye')

    agree = st.checkbox('I agree')

    if agree:
        st.write('Great!')

    genre = st.radio(
        "What\'s your favorite movie genre",
        ('Comedy', 'Drama', 'Documentary'))

    if genre == 'Comedy':
        st.write('You selected comedy.')
    else:
        st.write("You didn\'t select comedy.")

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.horizontal = False

    col1, col2 = st.columns(2)

    with col1:
        inner_cols = st.columns([1,1])
        with inner_cols[0]:
            st.checkbox("Disable radio widget", key="disabled")
            st.checkbox("Orient radio options horizontally", key="horizontal")
        with inner_cols[1]:
            st.radio(
            "Set label visibility 👇",
            ["visible", "hidden", "collapsed"],
            key="visibility",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            horizontal=st.session_state.horizontal,
        )

    with col2:
        inner_cols = st.columns([1,1])
        with inner_cols[0]:
            st.write('__This is inner1__')
        with inner_cols[1]:
            st.write('__This is inner2__')

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    options = st.multiselect(
        'What are your favorite colors',
        ['Green', 'Yellow', 'Red', 'Blue'],
        ['Yellow', 'Red'])

    st.write('You selected:', options)

    age = st.slider('How old are you?', 0, 130, 25)
    st.write("I'm ", age, 'years old')

    d = st.date_input(
        "When\'s your birthday",
        datetime.date(2019, 7, 6))
    st.write('Your birthday is:', d)

    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)

    color = st.color_picker('Pick A Color', '#00f900')
    st.write('The current color is', color)

    df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

    st.dataframe(df)  # Same as st.write(df)

    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

    st.metric(label="Gas price", value=4, delta=-0.5,
        delta_color="inverse")

    st.metric(label="Active developers", value=123, delta=123,
        delta_color="off")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.json({
        'foo': 'bar',
        'baz': 'boz',
        'stuff': [
            'stuff 1',
            'stuff 2',
            'stuff 3',
            'stuff 5',
        ],
    })    

    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    data = np.random.randn(10, 1)

    tab1.subheader("A tab with a chart")
    tab1.line_chart(data)

    tab2.subheader("A tab with the data")
    tab2.write(data)

    with st.expander("See explanation"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
        st.image("https://static.streamlit.io/examples/dice.jpg")

    container = st.container()
    container.write("Line 1")
    st.write("Line 2")

    # Now insert some more in the container
    container.write("Line 3")

if __name__ == "__main__":
    main()
