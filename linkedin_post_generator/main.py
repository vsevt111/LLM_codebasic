# This is a sample Python script.
import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# length_option=["Short","Medium","Long"]
# language_options=["English","Hinglish"]
# selected_influencer= "Akshat Shrivastava"
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def main():
    st.title("LinkedIn Post Generator")

    fs = FewShotPosts()
    selected_influencer = st.selectbox("Influencer", options=fs.get_influencer())
    if selected_influencer:
        fs_selected = FewShotPosts(selected_influencer)

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag=st.selectbox("Title",options=fs_selected.get_tags())
    with col2:
        selected_length=st.selectbox("Length",options=fs_selected.get_length())
    with col3:
        selected_langauge=st.selectbox("Language",options=fs_selected.get_language())


    if st.button("Generate"):
        post=generate_post(selected_length,selected_langauge,selected_tag)
        st.write(post)
        # st.write(f"Generated post for {selected_tag}, {selected_length}, {selected_langauge}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
