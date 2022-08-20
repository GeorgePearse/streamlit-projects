import streamlit as st
from streamlit_drawable_canvas import st_canvas
import tempfile
import itertools as IT
import os
from skimage.io import imsave


def uniquify(path, sep = ''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s = sep, n = next(count))
    orig = tempfile._name_sequence 
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir = dirname, prefix = filename, suffix = ext)
        tempfile._name_sequence = orig
    return filename


# "with" notation
with st.sidebar:
    # just render a readme file?
    st.write("""
    # Quicker Draw

    Google made the quick ML application QuickDraw. 
    I made this. 
    Write up on the background and motivation to this project is available on medium here. 

    https://medium.com/@george.pearse

    (hint, I'm looking for a job)

    Streamlit is not great at interactivity. Same button for refresh and submit 
    and I'll deal with any horrible data that crops up.

    Tempted to try a form of confident learning where I only accept images the 
    model is already confident on to retrain. This will enable a gradual evolution
    of the training set but will probably fall over on significantly different doodles.
    
    e.g. a car drawn from head on or similar.

    For the timebeing you have to save and submit as two separate steps.
    """)

target_item = 'moon'
st.write(f'# {target_item}')


# tempting
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=10,
    background_color="#eee",
    background_image=None,
    height=800,
    width=800,
    drawing_mode='freedraw',
    key="canvas",
)

st.write('# Display Input')

submitted = st.button('Submit')

if submitted: 
    st.image(canvas_result.image_data)

    file_path = f'./data/{target_item}/{target_item}.png'
    unique_file_path = uniquify(file_path)
    try:
        imsave(
            unique_file_path, 
            canvas_result.image_data
        )
        #dbx.files_upload(image_png, unique_file_path)
    except Exception as e:
        st.error(e)