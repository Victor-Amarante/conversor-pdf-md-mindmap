import os
import pathlib
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

BASE_DIR = os.getcwd()
DOCS_DIR = os.path.join(BASE_DIR, "docs")
MARKDOWN_DIR = os.path.join(BASE_DIR, "markdown")

file_in_docs_dir = "PGP-07_Gerência do Custo.pdf"
path_of_pdf = os.path.join(DOCS_DIR, file_in_docs_dir)

loader = PyPDFLoader(path_of_pdf)
documents = loader.load()

text_extratcted = ''.join(page.page_content for page in documents)
  
print("Text extracted")

def generate_mindmap_with_gpt(text):
    prompt = (
        "Use a sintaxe Markdown para organizar o conteúdo."
        "Organize o seguinte texto em um formato de mapa mental hierárquico:\n\n"
        f"{text}\n\n"
        "Use marcadores e subtópicos para organizar o conteúdo."
        "Quero o máximo de informações e detalhes que sejam relevantes para o estudo e apresentação do tema."
        "Não inclua nenhum texto que não seja relevante ao tema."
        "Não utilize nomes de professores, datas, números de versão ou qualquer outra informação que não seja relevante ao tema."
        "Faça um enriquecimento das informações desse markdown para criar um mindmap organizado e rico em conhecimento."
        "Remova os marcadores ``` e ``` que não são necessários."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
  
generate_mindmap_with_gpt(text_extratcted)

def save_markdown(markdown_text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_text)

def main():
    mindmap_text = generate_mindmap_with_gpt(text_extratcted)
    file_renamed = pathlib.Path(file_in_docs_dir).stem
    output_md_path = os.path.join(MARKDOWN_DIR, f"mindmap-{file_renamed}.md")
    save_markdown(mindmap_text, output_md_path)
    
    print(f"Mindmap salvo em: {output_md_path}")

if __name__ == "__main__":
    main()
