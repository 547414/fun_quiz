import logging.config

logging_config = {
  "version": 1,
  "disable_existing_loggers": None,
  "formatters": {
    "default": {
      "()": "uvicorn.logging.DefaultFormatter",
      "fmt": "%(asctime)s - %(levelprefix)s %(message)s",
      "use_colors": None
    },
    "access": {
      "()": "uvicorn.logging.AccessFormatter",
      "fmt": "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    }
  },
  "handlers": {
    "default": {
      "formatter": "default",
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stderr"
    },
    "access": {
      "formatter": "access",
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stdout"
    }
  },
  "loggers": {
    "uvicorn": {
      "handlers": [
        "default"
      ],
      "level": "INFO"
    },
    "uvicorn.error": {
      "level": "INFO"
    },
    "uvicorn.access": {
      "handlers": [
        "access"
      ],
      "level": "INFO",
      "propagate": False
    }
  }
}

logging.config.dictConfig(logging_config)
