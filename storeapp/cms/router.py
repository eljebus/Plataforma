class cms(object):
    def db_for_read(self, model, **hints):
        """
        Attempts to read cms models go to cms.
        """
        if model._meta.app_label == 'cms':
            return 'cms'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write cms models go to cms.
        """
        if model._meta.app_label == 'cms':
            return 'cms'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the cms app is involved.
        """
        if obj1._meta.app_label == 'cms' or \
           obj2._meta.app_label == 'cms':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the cms app only appears in the 'cms'
        database.
        """
        if db == 'cms':
            return model._meta.app_label == 'cms'
        elif model._meta.app_label == 'cms':
            return False
        return None