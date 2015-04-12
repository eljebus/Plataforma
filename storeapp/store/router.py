
class Store(object):
    """
    A router to control all database operations on models in the
    store application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read store models go to default.
        """
        if model._meta.app_label == 'store':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write store models go to default.
        """
        if model._meta.app_label == 'store':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the store app is involved.
        """
        if obj1._meta.app_label == 'store' or \
           obj2._meta.app_label == 'store':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the store app only appears in the 'default'
        database.
        """
        if db == 'default':
            return model._meta.app_label == 'store'
        elif model._meta.app_label == 'store':
            return False
        return None
