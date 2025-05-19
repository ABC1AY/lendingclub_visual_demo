import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# 支持的图类型
plot_types = ["Bar Plot", "Box Plot", "Scatter Plot", "Heatmap"]


def process_file():
    # read
    df = pd.read_csv("accepted_2007_to_2018Q4.csv", low_memory=False)

    # clean data
    useful_cols = ["loan_amnt", "term", "int_rate", "grade", "sub_grade",
                   "emp_length", "home_ownership", "annual_inc",
                   "loan_status", "purpose"]
    df = df[[col for col in useful_cols if col in df.columns]]

    df['int_rate'] = df['int_rate'].astype(float)

    df.dropna(inplace=True)

    return df


#visualisation
def generate_plot(df, plot_type, x_col, y_col=None):
    plt.figure(figsize=(10, 6))

    if plot_type == "Bar Plot":
        sns.countplot(data=df, x=x_col)
    elif plot_type == "Box Plot":
        sns.boxplot(data=df, x=x_col, y=y_col)
    elif plot_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_col, y=y_col)
    elif plot_type == "Heatmap":
        corr = df.select_dtypes(include='number').corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")

    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


# 主函数：上传文件 + 交互式图表
def main(plot_type, x_col, y_col):
    df = process_file()
    img = generate_plot(df, plot_type, x_col, y_col)
    return img


# 动态更新列选项



# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("#Lending Club 金融数据可视化工具")
    gr.Markdown("选择图表类型和列，自动生成可视化图表")

    with gr.Row():
        plot_dropdown = gr.Dropdown(plot_types, label="选择图表类型")

    with gr.Row():
        x_col = gr.Dropdown(choices=[], label="X 轴列")
        y_col = gr.Dropdown(choices=[], label="Y 轴列（部分图可为空）")

    btn_plot = gr.Button("生成图表")
    image_output = gr.Image(label="可视化图表")


    # 按钮点击生成图表
    btn_plot.click(fn=main, inputs=[plot_dropdown, x_col, y_col], outputs=image_output)

demo.launch()
