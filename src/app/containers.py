import logging

from a8t_tools.storage.local_storage import LocalStorageBackend
from celery import Celery

from a8t_tools.bus.consumer import setup_consumers
from a8t_tools.bus.producer import TaskProducer
from a8t_tools.bus.scheduler import setup_schedule
from dependency_injector import containers, providers
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import UnitOfWork
from a8t_tools.logging.utils import setup_logging
from a8t_tools.bus.celery import CeleryBackend

from app.config import Settings
from app.domain.users.containers import UserContainer


class Container(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    config.from_dict(
        options=Settings(_env_file=".env", _env_file_encoding="utf-8").model_dump(),  # type: ignore [call-arg]
    )

    logging = providers.Resource(
        setup_logging,
        logger_level=logging.INFO,
        sentry_dsn=config.sentry.dsn,
        sentry_environment=config.sentry.env_name,
        sentry_traces_sample_rate=config.sentry.traces_sample_rate,
        json_logs=False,
    )

    transaction = providers.Singleton(AsyncDbTransaction, dsn=config.db.dsn)

    unit_of_work = providers.Factory(UnitOfWork, transaction=transaction)

    celery_app: providers.Provider[Celery] = providers.Singleton(Celery, "worker", broker=config.mq.broker_uri)

    celery_backend = providers.Factory(CeleryBackend, celery_app=celery_app)

    tasks_backend = celery_backend

    consumers = providers.Resource(setup_consumers, tasks_backend=tasks_backend, tasks_params=config.tasks.params)

    tasks_scheduler = celery_backend

    schedules = providers.Resource(setup_schedule, scheduler=tasks_scheduler, raw_schedules=config.tasks.schedules)

    task_producer = providers.Factory(TaskProducer, backend=tasks_backend)

    local_storage_backend = providers.Factory(
        LocalStorageBackend,
        base_path=config.storage.local_storage.base_path,
        base_uri=config.storage.local_storage.base_uri,
    )

    user = providers.Container(
        UserContainer,
        transaction=transaction,
        task_producer=task_producer,
        secret_key=config.security.secret_key,
        private_key=config.security.private_key,
        public_key=config.security.public_key,
        pwd_context=config.security.pwd_context,
        access_expiration_time=config.security.access_expiration_min,
        refresh_expiration_time=config.security.refresh_expiration_min,
    )
