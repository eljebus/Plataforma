class AdminRouter(object):
    """
    A router to control all database operations on models in the
    admin application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read admin models go to usuario.
        """
        if model._meta.app_label == 'admin':
            return 'usuario'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write admin models go to usuario.
        """
        if model._meta.app_label == 'admin':
            return 'usuario'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the admin app is involved.
        """
        if obj1._meta.app_label == 'admin' or \
           obj2._meta.app_label == 'admin':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the admin app only appears in the 'usuario'
        database.
        """
        if db == 'usuario':
            return model._meta.app_label == 'admin'
        elif model._meta.app_label == 'admin':
            return False
        return None