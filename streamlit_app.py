# pip install streamlit
import streamlit as st
from st_init import init


def main():
    st.text("合同会社ＳＡＴ")
    st.subheader("作業報告アプリ🐗🦌🦋")
    st.write('左上の"＞"でメニューを表示')
    st.write("---")


def user_select():
    users_df = st.session_state.users
    user_options = list({u["user_name"] for u in users_df})

    # UI切り替え用のフラグ
    if "show_selectbox" not in st.session_state:
        st.session_state.show_selectbox = False

    # 既にユーザーが選択されている場合
    if "user" in st.session_state and st.session_state.user:
        user_info = st.session_state.user
        user_name = user_info.get("user_name", str(user_info))
        st.success(f"ログインユーザー：{user_name}")
        if st.button("ユーザー変更"):
            st.session_state.user = None
            st.session_state.show_selectbox = False
            st.session_state.params_user = None
            st.rerun()
        else:
            return

    # アプリアクセスクエリによるユーザーコード取得
    # elif st.session_state.params_user is not None:
    #     # st.session_state.users の["params_user"]で検索して一致するレコードを取得
    #     st.session_state.user = next(
    #         (
    #             u
    #             for u in st.session_state.users
    #             if u["params_user"] == st.session_state.params_user
    #         ),
    #         None,
    #     )
    #     user_name = st.session_state.user.get("user_name", str(st.session_state.user))
    #     st.success(f"ログインユーザー：{user_name}")
    #     if st.button("ユーザー変更"):
    #         st.session_state.user = None
    #         st.session_state.show_selectbox = False
    #         st.session_state.params_user = None
    #         st.rerun()
    #     else:
    #         return

    # プルダウン選択表示
    elif st.session_state.show_selectbox:
        with st.form("selectbox_form"):
            selected_user_name = st.selectbox(
                "ユーザーを選択", user_options, key="selectbox_user"
            )
            selectbox_submitted = st.form_submit_button("ログイン")
        if selectbox_submitted:
            # レコード取得
            user_record = next(
                u for u in users_df if u["user_name"] == selected_user_name
            )
            st.session_state.user = user_record
            st.success(f"ログインユーザー：{selected_user_name}")
            return
        if st.button("直接入力へ"):
            st.session_state.show_selectbox = False
            st.rerun()

    # フォーム入力表示
    else:
        with st.form("user_input_form"):
            input_user = st.text_input("ユーザー名を入力（完全一致）")
            submitted = st.form_submit_button("ログイン")
        if st.button("選択肢入力へ"):
            st.session_state.show_selectbox = True
            st.rerun()
        if submitted:
            if input_user and input_user in user_options:
                # レコード取得
                user_record = next(u for u in users_df if u["user_name"] == input_user)
                st.session_state.user = user_record
                st.success(f"ログインユーザー：{input_user}")
            else:
                st.error(
                    "ユーザー名が見つかりません。正しいユーザー名を入力してください。"
                )


if __name__ == "__main__":
    init()
    main()
    user_select()
