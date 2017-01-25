from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('username')
            table.string('email').unique()
            table.string('first_name').default('').nullable()
            table.string('last_name').default('').nullable()
            table.string('country').default('').nullable()
            table.string('city').default('').nullable()
            table.string('phone').default('').nullable()
            table.string('password')
            table.boolean('is_admin').default(0)
            table.boolean('is_active').default(1)
            table.integer('company_id').unsigned().index().nullable()
            table.foreign('company_id').references('id').on('companies').on_delete('CASCADE')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            table.drop_foreign('users_company_id_foreign')

        self.schema.drop('users')
