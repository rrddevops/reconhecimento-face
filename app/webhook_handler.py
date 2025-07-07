import httpx
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

class WebhookHandler:
    def __init__(self):
        self.webhook_url = os.getenv('WEBHOOK_URL', 'http://192.168.5.67:8000/webhook')
        self.enable_logging = os.getenv('WEBHOOK_LOGGING', 'true').lower() == 'true'
        self.timeout = int(os.getenv('WEBHOOK_TIMEOUT', '10'))
    
    async def enviar_reconhecimento(self, cpf: str, dados_adicionais: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia webhook quando usuário é reconhecido
        
        Args:
            cpf: CPF do usuário reconhecido
            dados_adicionais: Dados extras para incluir no webhook
            
        Returns:
            bool: True se webhook foi enviado com sucesso
        """
        payload = {
            "cpf": cpf
        }
        
        if dados_adicionais:
            payload.update(dados_adicionais)
        
        print(f"Tentando enviar webhook para: {self.webhook_url}")
        print(f"Payload: {payload}")
        
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"}
                )
                
                if self.enable_logging:
                    print(f"Webhook enviado para CPF {cpf}: {response.status_code}")
                    if response.status_code not in [200, 201, 202]:
                        print(f"Erro no webhook: {response.text}")
                        print(f"URL final: {response.url}")
                
                return response.status_code in [200, 201, 202]
                
        except httpx.TimeoutException:
            if self.enable_logging:
                print(f"Timeout ao enviar webhook para CPF {cpf}")
            return False
        except Exception as e:
            if self.enable_logging:
                print(f"Erro ao enviar webhook para CPF {cpf}: {e}")
            return False
    


# Instância global do webhook handler
webhook_handler = WebhookHandler() 