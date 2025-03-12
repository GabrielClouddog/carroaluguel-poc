import streamlit as st
import requests
import uuid
import json

ENDPOINT_URL = "https://ggjtv6yy7d.execute-api.us-east-1.amazonaws.com/stg/chat"

st.title("💬 Chatbot")

# Definir o modelo fixo
chosen_model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Gerar um UUID único para o cliente
if "customer_id" not in st.session_state:
    st.session_state["customer_id"] = str(uuid.uuid4())

customer_id = st.session_state["customer_id"]

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Como posso ajudar você?"}
    ]

# Exibir mensagens anteriores
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Criar uma aba para copiar JSON
with st.sidebar:
    st.header("Copiar JSON")
    retirada_data = json.dumps({"tipo_retirada": "bairro", "ref_retirada": "reboucas", "cid_retirada": 6015}, indent=4)
    devolucao_data = json.dumps({"tipo_devolucao": "aeroporto", "ref_devolucao": 9, "cid_devolucao": 8452}, indent=4)
    
    if st.button("Copiar LOCAL_RETIRADA"):
        st.session_state["copied_json"] = retirada_data
    if st.button("Copiar LOCAL_DEVOLUCAO"):
        st.session_state["copied_json"] = devolucao_data
    
    if "copied_json" in st.session_state:
        st.code(st.session_state["copied_json"], language="json")

# Aguardar a entrada do usuário
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Preparar os dados da solicitação
    request_data = {
        "Question": prompt,  # A questão é o que o usuário digitou
        "CustomerId": customer_id,  # Usar o ID do cliente gerado automaticamente
    }

    print('request_data', request_data)

    try:
        # Enviar a solicitação para a API
        response = requests.post(ENDPOINT_URL, json=request_data)
        print("RESPONSE::: ", response)
        if response.status_code == 200:
            response_data = response.json()
            print("RESPONSE: ", response_data)

            # Extrair o campo "output" da resposta
            response_output = response_data.get("output", {})

            response_text = response_output.get("question", "Resposta não encontrada.")
            response_type = response_output.get("type", "Tipo não especificado")

            # Formatar a resposta para incluir o tipo
            formatted_response = f"[{response_type}] | {response_text}"

            # Adicionar a resposta ao histórico de mensagens
            st.session_state.messages.append(
                {"role": "assistant", "content": formatted_response}
            )
            st.chat_message("assistant").write(formatted_response)

            print(f"Response data: {response_data}")
        else:
            st.error("Falhou em obter uma resposta da API.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar enviar o pedido: {e}")