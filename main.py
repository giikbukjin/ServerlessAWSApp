import gradio as gr
import pandas as pd

# CSV 파일 경로
csv_file = "AccountBook.csv"

# 데이터 조회 함수
def read_fn():
    df = pd.read_csv(csv_file)
    return df

# 데이터 입력 함수
def create_fn(div, date, description, amount, category, memo):
    df = read_fn()
    entry = pd.DataFrame({"분류": [div], "날짜": [date], "항목": [description], "금액": [amount], "카테고리": [category], "메모": [memo]})
    df = pd.concat([df, entry], ignore_index = True)
    write(df)
    return "입력이 완료되었습니다."

def write(df):
    df.to_csv(csv_file, index = False)

# 데이터 수정 함수
def update_fn(index, div, date, description, amount, category, memo):
    df = read_fn()
    if index < len(df):
        df.loc[index] = [div, date, description, amount, category, memo]
        write(df)
    return "수정이 완료되었습니다."

# 데이터 삭제 함수
def delete_fn(index):
    df = read_fn()
    if index < len(df):
        df = df.drop(index = index)
        df.reset_index(drop = True, inplace = True)
        write(df)
    return "삭제가 완료되었습니다."


# Gradio UI 인터페이스
with gr.Blocks() as demo:
    gr.Markdown("가계부 프로그램")

    with gr.Tab("조회"):
        read_input = None
        read_output = gr.outputs.Dataframe(type = "pandas")
        read_button = gr.Button("저장")

    with gr.Tab("입력"):
        create_input = [
            gr.inputs.Radio(choices = ["수입", "지출"], label = "동작"),
            gr.inputs.Textbox(label = "날짜"), 
            gr.inputs.Textbox(label = "항목"),
            gr.inputs.Textbox(label = "금액"),
            gr.inputs.Dropdown(choices = ["수입", "식비", "교통비", "통신비", "주거비", "문화비", "저축", "기타"], label = "카테고리"),
            gr.inputs.Textbox(label = "메모"),
        ]
        create_output = gr.Textbox(label = "결과")
        create_button = gr.Button("저장")

    with gr.Tab("수정"):
        update_input = [
            gr.inputs.Radio(choices = ["수입", "지출"], label = "동작"),
            gr.inputs.Textbox(label = "날짜"), 
            gr.inputs.Textbox(label = "항목"),
            gr.inputs.Textbox(label = "금액"),
            gr.inputs.Dropdown(choices = ["수입", "식비", "교통비", "통신비", "주거비", "문화비", "저축", "기타"], label = "카테고리"),
            gr.inputs.Textbox(label = "메모"),
            gr.inputs.Number(label = "인덱스(0부터 시작)")
        ]
        update_output = gr.Textbox(label = "결과")
        update_button = gr.Button("저장")

    with gr.Tab("삭제"):
        delete_input =  gr.inputs.Number(label = "인덱스")
        delete_output = gr.Textbox(label = "결과")
        delete_button = gr.Button("저장")


    read_button.click(
        fn = read_fn, 
        inputs = read_input, 
        outputs = read_output
    )
    create_button.click(
        fn = create_fn, 
        inputs = create_input, 
        outputs = create_output
    )
    update_button.click(
        fn = update_fn, 
        inputs = update_input, 
        outputs = update_output
    )
    create_button.click(
        fn = delete_fn, 
        inputs = delete_input, 
        outputs = delete_output
    )
demo.launch()