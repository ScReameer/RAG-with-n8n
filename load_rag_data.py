from pathlib import Path
import requests


def load_rag_data() -> None:
    """
    Loads the RAG data from files and encodes the chunks using the encoder.
    """
    rag_data_path = Path('rag_data')
    encoder_endpoint = 'http://0.0.0.0:8080/embed'
    rag_data: dict[str, list] = {"vectors": []}

    for file in rag_data_path.iterdir():
        if file.is_file():
            with open(file, 'r') as f:
                chunks = f.read().split('\n\n')
            for chunk_number, chunk in enumerate(chunks):
                chunk = chunk.replace('\n', ' ')
                resp = requests.post(encoder_endpoint, json={"text": chunk})
                embedding = resp.json()['embedding']
                rag_data['vectors'].append(
                    {
                        "id": f"{file.stem}_chunk_{chunk_number}",
                        "values": embedding,
                        "metadata": {"text": chunk}
                    }
                )

    res = requests.post("http://0.0.0.0:5081/vectors/upsert", json=rag_data)
    print(f'Status code: {res.status_code}\nResponse: {res.text}')

if __name__ == "__main__":
    load_rag_data()