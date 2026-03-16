import streamlit as st
import pandas as pd





st.set_page_config(page_title="Sắp xếp công việc", page_icon="✅", layout="centered")

st.title("📋 Sắp xếp danh sách công việc")
st.write(
    "Tải lên file Excel chứa danh sách công việc, "
    "sau đó chọn tiêu chí sắp xếp và chiều sắp xếp để xem kết quả."
)


@st.cache_data
def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)


st.subheader("1. Tải file Excel danh sách công việc")
uploaded_file = st.file_uploader(
    "Chọn file Excel (.xlsx, .xls)",
    type=["xlsx", "xls"],
)

if uploaded_file is None:
    st.info("Vui lòng chọn một file Excel để tiếp tục.")
else:
    try:
        df = load_excel(uploaded_file)
    except Exception as e:
        st.error(f"Không đọc được file Excel. Chi tiết lỗi: {e}")
        df = pd.DataFrame()

    if df.empty:
        st.warning("File Excel không có dữ liệu (hoặc chỉ có tiêu đề). Hãy kiểm tra lại.")
    else:
        st.write("Xem nhanh dữ liệu gốc:")
        st.dataframe(df, use_container_width=True)

        st.subheader("2. Chọn cách sắp xếp")

        sort_column = st.selectbox(
            "Sắp xếp theo cột:",
            options=list(df.columns),
            index=0,
        )

        sort_order_label = st.radio(
            "Thứ tự sắp xếp:",
            options=["Tăng dần (nhỏ → lớn / A → Z)", "Giảm dần (lớn → nhỏ / Z → A)"],
            index=0,
            horizontal=True,
        )
        ascending = sort_order_label.startswith("Tăng dần")

        st.subheader("3. Kết quả sau khi sắp xếp")

        sorted_df = df.sort_values(by=sort_column, ascending=ascending).reset_index(
            drop=True
        )
        st.dataframe(sorted_df, use_container_width=True, height=350)

        st.download_button(
            "📥 Tải kết quả dạng CSV",
            data=sorted_df.to_csv(index=False, encoding="utf-8-sig"),
            file_name="cong_viec_da_sap_xep.csv",
            mime="text/csv",
        )

