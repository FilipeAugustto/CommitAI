from google import genai
from schemas import CommitSchema
from settings import Config
from utils import PROMPT

cfg = Config()
client = genai.Client(api_key=cfg.API_KEY.get_secret_value())


def main():
    print('Bem-vindo ao CommitAI')
    print(
        'Descreva as mudanças que você realizou '
        'no código para que o commit seja gerado'
    )
    user_desc = input('Descrição: ')

    interaction = client.interactions.create(
        model=cfg.MODELO,
        system_instruction=PROMPT,
        input=user_desc,
        store=False,
        generation_config={
            'max_output_tokens': cfg.MAX_TOKENS,
            'thinking_level': cfg.THINKING_LEVEL,
        },
        response_format={
            'type': 'text',
            'mime_type': 'application/json',
            'schema': CommitSchema.model_json_schema(),
        },
    )

    commit = CommitSchema.model_validate_json(interaction.output_text)
    print(commit.formatar())


if __name__ == '__main__':
    main()
