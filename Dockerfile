# Imagem base oficial do Python slim para menor superfície de ataque e tamanho reduzido
FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="MBA DataOps Team" \
      description="Pipeline de Conciliação Contábil e Auditoria de Roteiros"

# Variáveis de ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Diretório de trabalho
WORKDIR /app

# Instalação de dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas os arquivos de requisitos para aproveitar cache de camadas
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo o código fonte da aplicação
COPY . .

# Criar usuário sem privilégios de root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Porta exposta pelo Flask / Gunicorn
EXPOSE 5000

# Healthcheck para monitorar o status do container
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando padrão de inicialização com Gunicorn para produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
