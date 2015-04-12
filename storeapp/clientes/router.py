class Client(object):
    def db_for_read(self, model, **hints):
        """
        Attempts to read client models go to client.
        """
        if model._meta.app_label == 'clientes':
            return 'client'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write client models go to client.
        """
        if model._meta.app_label == 'clientes':
            return 'client'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the client app is involved.
        """
        if obj1._meta.app_label == 'clientes' or \
           obj2._meta.app_label == 'clientes':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the client app only appears in the 'client'
        database.
        """
        if db == 'client':
            return model._meta.app_label == 'clientes'
        elif model._meta.app_label == 'clientes':
            return False
        return None
        