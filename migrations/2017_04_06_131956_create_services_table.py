from orator.migrations import Migration


class CreateServicesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('services') as table:
            table.increments('id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('services')
