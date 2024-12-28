from src.utils.audio_recorder import record_audio
from src.graph.workflow import get_graph


def receive_message():
    graph = get_graph()

    while True:
        message = input("Você: ")
        if message.lower() == "sair":
            print("Encerrando o chat...", flush=True)
            break

        if message.lower() == "record":
            message = str(record_audio())

        output = graph.invoke({"messages": [message]})
        print(f"Assistente: {output['messages'][-1].content}")


if __name__ == "__main__":
    receive_message()
