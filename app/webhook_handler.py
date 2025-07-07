import httpx
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class WebhookHandler:
    def __init__(self):
        self.webhook_url = os.getenv('WEBHOOK_URL', 'http://172.16.10.152:8000/webhook')
        self.enable_logging = os.getenv('WEBHOOK_LOGGING', 'true').lower() == 'true'
        self.timeout = int(os.getenv('WEBHOOK_TIMEOUT', '10'))
        # Cache para evitar reenvios duplicados (CPF -> timestamp do último envio)
        self.sent_webhooks = {}
        # Tempo mínimo entre webhooks para o mesmo CPF (em segundos)
        self.min_interval = int(os.getenv('WEBHOOK_MIN_INTERVAL', '300'))  # 5 minutos por padrão
    
    async def enviar_reconhecimento(self, cpf: str, dados_adicionais: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia webhook quando usuário é reconhecido
        
        Args:
            cpf: CPF do usuário reconhecido
            dados_adicionais: Dados extras para incluir no webhook
            
        Returns:
            bool: True se webhook foi enviado com sucesso
        """
        # Verificar se já foi enviado recentemente
        now = datetime.now()
        if cpf in self.sent_webhooks:
            last_sent = self.sent_webhooks[cpf]
            time_diff = (now - last_sent).total_seconds()
            
            if time_diff < self.min_interval:
                remaining_time = self.min_interval - time_diff
                if self.enable_logging:
                    print(f"Webhook para CPF {cpf} ignorado - enviado há {time_diff:.1f}s (mínimo: {self.min_interval}s)")
                    print(f"Próximo envio permitido em {remaining_time:.1f} segundos")
                return False
        
        payload = {
            "cpf": cpf,
            "timestamp": now.isoformat(),
            "detection_id": f"{cpf}_{now.strftime('%Y%m%d_%H%M%S')}"
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
                
                # Se enviou com sucesso, registrar no cache
                if response.status_code in [200, 201, 202]:
                    self.sent_webhooks[cpf] = now
                    if self.enable_logging:
                        print(f"Webhook para CPF {cpf} registrado no cache")
                
                return response.status_code in [200, 201, 202]
                
        except httpx.TimeoutException:
            if self.enable_logging:
                print(f"Timeout ao enviar webhook para CPF {cpf}")
            return False
        except Exception as e:
            if self.enable_logging:
                print(f"Erro ao enviar webhook para CPF {cpf}: {e}")
            return False
    
    def limpar_cache_antigo(self, max_age_hours: int = 24):
        """
        Remove entradas antigas do cache de webhooks
        
        Args:
            max_age_hours: Idade máxima em horas para manter no cache
        """
        now = datetime.now()
        max_age = timedelta(hours=max_age_hours)
        
        cpf_to_remove = []
        for cpf, timestamp in self.sent_webhooks.items():
            if now - timestamp > max_age:
                cpf_to_remove.append(cpf)
        
        for cpf in cpf_to_remove:
            del self.sent_webhooks[cpf]
        
        if cpf_to_remove and self.enable_logging:
            print(f"Removidos {len(cpf_to_remove)} CPFs antigos do cache de webhooks")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        Retorna status do cache de webhooks
        
        Returns:
            Dict com informações do cache
        """
        now = datetime.now()
        cache_info = {
            "total_entries": len(self.sent_webhooks),
            "min_interval_seconds": self.min_interval,
            "entries": {}
        }
        
        for cpf, timestamp in self.sent_webhooks.items():
            time_diff = (now - timestamp).total_seconds()
            cache_info["entries"][cpf] = {
                "last_sent": timestamp.isoformat(),
                "seconds_ago": time_diff,
                "can_send_again": time_diff >= self.min_interval
            }
        
        return cache_info
    


# Instância global do webhook handler
webhook_handler = WebhookHandler() 