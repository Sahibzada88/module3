import gradio as gr
from eg import chain

with gr.Blocks(title="ChatGpt Clone") as demo:
    gr.Markdown("# Chatgpt 4 Clone")
    with gr.Row():
        gr.Markdown("")
        with gr.Column(scale=6):
            chatbox = gr.Chatbot(type="messages")
            with gr.Row():
                textbox = gr.Textbox(scale=7,container=False, placeholder="Ask question")
                submit = gr.Button(value="Submit", scale=3, variant="primary")
        gr.Markdown("")


    def chatbot(question, history):
        history.append({"role":"user", "content":question})
        if question == "":
            response = "Please ask question"
            history.append({"role":"assistant", "content": response})
        else:
            response = chain.stream(question)
            history.append({"role":"assistant", "content": ""}) 
        for i in response:
            history[-1]['content'] += i
            yield "", history

    textbox.submit(chatbot, inputs=[textbox, chatbox], outputs=[textbox, chatbox])
    submit.click(chatbot, inputs=[textbox, chatbox], outputs=[textbox, chatbox])

    
#gr.ChatInterface( fn=chatbot, type="messages" ).launch()

demo.launch(
    share=True
)            