from orator.migrations import Migration


class CreateCompaniesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('companies') as table:
            table.increments('id')
            table.string('name')
            table.string('address')
            table.string('logo').nullable().default('')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('companies')
