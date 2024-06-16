import pytest
import asyncio
from unittest.mock import patch, MagicMock
from aioresponses import aioresponses
from main import main

@pytest.mark.asyncio
async def test_main():
    with patch('main.init_db', new_callable=MagicMock) as mock_init_db:
        mock_init_db.return_value = asyncio.Future()
        mock_init_db.return_value.set_result(None)

        with aioresponses() as m:
            url = "https://swapi.dev/api/people/"
            characters_data = [
                {"name": "Character1", "id": 1},
                {"name": "Character2", "id": 2},
            ]
            m.get(url, payload={"results": characters_data})

            with patch('main.fetch_characters', new_callable=MagicMock) as mock_fetch_characters:
                mock_fetch_characters.return_value = asyncio.Future()
                mock_fetch_characters.return_value.set_result(characters_data)

                with patch('main.SessionLocal', new_callable=MagicMock) as mock_session:
                    mock_session_instance = mock_session.return_value
                    mock_session_instance.__aenter__.return_value = mock_session_instance
                    mock_session_instance.__aexit__.return_value = asyncio.Future()
                    mock_session_instance.__aexit__.return_value.set_result(None)

                    with patch('main.add_character', new_callable=MagicMock) as mock_add_character:
                        mock_add_character.return_value = asyncio.Future()
                        mock_add_character.return_value.set_result(None)

                        await main()

                        mock_init_db.assert_called_once()
                        mock_fetch_characters.assert_called_once()
                        assert mock_add_character.call_count == len(characters_data)
                        for character in characters_data:
                            mock_add_character.assert_any_call(mock_session_instance, character)

if __name__ == '__main__':
    asyncio.run(test_main())