from orator.migrations import Migration
from db import db
from test_db import db as test_db

class CreateProjectsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('projects') as table:
            table.increments('id')
            table.string('title')
            table.text('description').default('')
            table.decimal('price', 10, 2)
            table.string('longitude')
            table.string('latitude')
            table.boolean('published').default(True)
            table.integer('company_id').unsigned().index().nullable()
            table.foreign('company_id').references('id').on('companies').on_delete('CASCADE')
            table.timestamps()



    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('projects') as table:
            table.drop_foreign('projects_company_id_foreign')

        self.schema.drop('projects')

