import gradio as gr
import replicate
import os

# Função para gerar imagem realista
def gerar_realismo(prompt, api_key):
    if not api_key:
        return None, "Por favor, insira sua API Token do Replicate."
    os.environ["REPLICATE_API_TOKEN"] = api_key
    try:
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e24ee33373c9594456390f462867f6c82f8d569a9273",
            input={"prompt": prompt}
        )
        return output[0], "Sucesso!"
    except Exception as e:
        return None, f"Erro: {str(e)}"

# Função para Face Swap
def trocar_rosto(face_source, target_img, api_key):
    if not api_key:
        return None, "Insira a API Token."
    os.environ["REPLICATE_API_TOKEN"] = api_key
    try:
        output = replicate.run(
            "lucataco/faceswap:9a429854844a419c48f03f95458e5e1d204e963dc30f1c9763cc359237f59997",
            input={"target_image": target_img, "swap_image": face_source}
        )
        return output, "Troca realizada!"
    except Exception as e:
        return None, f"Erro: {str(e)}"

# Interface Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎭 IA Studio - FaceApp & Realismo")
    
    with gr.Row():
        api_input = gr.Textbox(label="Sua Replicate API Token", placeholder="r8_...", type="password")
    
    with gr.Tab("📸 Gerador Realista"):
        prompt_txt = gr.Textbox(label="O que você quer criar?", placeholder="Ex: Portrait of a futuristic warrior, 8k, realistic")
        btn_gen = gr.Button("Gerar Imagem")
        out_gen = gr.Image(label="Resultado")
        status_gen = gr.Textbox(label="Status")
        
        btn_gen.click(gerar_realismo, inputs=[prompt_txt, api_input], outputs=[out_gen, status_gen])

    with gr.Tab("🎭 Face Swap"):
        with gr.Row():
            src = gr.Image(label="Seu Rosto", type="filepath")
            tgt = gr.Image(label="Imagem de Destino", type="filepath")
        btn_swap = gr.Button("Trocar Rosto")
        out_swap = gr.Image(label="Rosto Trocado")
        status_swap = gr.Textbox(label="Status")
        
        btn_swap.click(trocar_rosto, inputs=[src, tgt, api_input], outputs=[out_swap, status_swap])

demo.launch()
