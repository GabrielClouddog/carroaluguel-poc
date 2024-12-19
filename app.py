import streamlit as st
import requests

ENDPOINT_URL = "https://pz8ly572of.execute-api.us-east-1.amazonaws.com/chat"

st.title("💬 Chatbot")

models = {
    "claude-v3-5-sonnet": "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "claude-v3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
}

model_id_options = list(models.keys())

selected_model_id = st.selectbox("Modelo", model_id_options)

# Obter o modelo selecionado
chosen_model_id = models[selected_model_id]

# Campo de entrada para CustomerId
customer_id = st.text_input("ID do Cliente")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Como posso ajudar você?"}
    ]

# Exibir mensagens anteriores
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Aguardar a entrada do usuário
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Preparar os dados da solicitação
    request_data = {
        "Question": prompt,  # A questão é o que o usuário digitou
        "CustomerId": customer_id,  # Usar o ID do cliente inserido
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
            response_text = response_data.get("output", "Resposta não encontrada.")

            # Adicionar a resposta ao histórico de mensagens
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            st.chat_message("assistant").write(response_text)

            print(f"Response data: {response_data}")
        else:
            st.error("Falhou em obter uma resposta da API.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar enviar o pedido: {e}")
