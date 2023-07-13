import gradio as gr
import pandas as pd

# CSV 파일 경로
csv_file = "AccountBook.csv"

# 데이터 조회 함수
def read():
    df = pd.read_csv(csv_file)
    return df

# 데이터 입력 함수
def create(date, description, amount, category, memo):
    df = read()
    entry = pd.DataFrame({"날짜": [date], "항목": [description], "금액": [amount], "카테고리": [category], "메모": [memo]})
    df = pd.concat([df, entry], ignore_index = True)
    write(df)
    return df

def write(df):
    df.to_csv(csv_file, index = False)

# 데이터 수정 함수
def update(index, date, description, amount, category, memo):
    df = read()
    if index < len(df):
        df.loc[index] = [date, description, amount, category, memo]
        write(df)
    return df

# 데이터 삭제 함수
def delete(index):
    df = read()
    if index < len(df):
        df = df.drop(index = index)
        df.reset_index(drop = True, inplace = True)
        write(df)
    return df


# Gradio 인터페이스
def gradio_interface(action, date, description, amount, category, memo, index = None):
    if action == "조회":
        return read()
    elif action == "입력":
        if date and description and amount:
            create(date, description, amount, category, memo)
        return read()
    elif action == "수정":
        update(index, date, description, amount, category, memo)
        return read()
    elif action == "삭제":
        delete(index)
        return read()

# Gradio UI 구성 요소
inputs = [
    gr.inputs.Dropdown(choices = ["조회", "입력", "수정", "삭제"], label = "동작"),
    gr.inputs.Textbox(label = "날짜"), 
    gr.inputs.Textbox(label = "항목"),
    gr.inputs.Textbox(label = "금액"),
    gr.inputs.Dropdown(choices = ["수입", "식비", "교통비", "통신비", "주거비", "문화비", "저축", "기타"], label = "카테고리"),
    gr.inputs.Textbox(label = "메모"),
    gr.inputs.Number(label = "인덱스 (수정 또는 삭제할 때만 필요)")
]

outputs = gr.outputs.Dataframe(type = "pandas")  # DataFrame 출력 요소

gr.Interface(
    fn = gradio_interface,
    inputs = inputs,
    outputs = outputs,
    title = "가계부 프로그램"
).launch(share = True)