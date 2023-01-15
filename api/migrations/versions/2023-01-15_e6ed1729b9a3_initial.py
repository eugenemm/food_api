"""initial

Revision ID: e6ed1729b9a3
Revises: 
Create Date: 2023-01-15 15:52:43.038151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6ed1729b9a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food_categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False, comment='Название'),
    sa.Column('is_publish', sa.Boolean(), nullable=False, comment='Опубликован'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_categories_id'), 'food_categories', ['id'], unique=True)
    op.create_index(op.f('ix_food_categories_name'), 'food_categories', ['name'], unique=True)
    op.create_table('toppings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False, comment='Название'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_toppings_id'), 'toppings', ['id'], unique=True)
    op.create_index(op.f('ix_toppings_name'), 'toppings', ['name'], unique=True)
    op.create_table('foods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=255), nullable=False, comment='Название'),
    sa.Column('description', sa.Unicode(length=255), nullable=True, comment='Описание'),
    sa.Column('price', sa.Integer(), nullable=False, comment='Цена'),
    sa.Column('is_special', sa.Boolean(), nullable=False, comment='Признак "особенный"'),
    sa.Column('is_vegan', sa.Boolean(), nullable=False, comment='Признак "для веганов"'),
    sa.Column('is_publish', sa.Boolean(), nullable=False, comment='Опубликован'),
    sa.Column('category_id', sa.Integer(), nullable=True, comment='идентификатор категории'),
    sa.ForeignKeyConstraint(['category_id'], ['food_categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_foods_category_id'), 'foods', ['category_id'], unique=False)
    op.create_index(op.f('ix_foods_description'), 'foods', ['description'], unique=False)
    op.create_index(op.f('ix_foods_id'), 'foods', ['id'], unique=True)
    op.create_index(op.f('ix_foods_name'), 'foods', ['name'], unique=True)
    op.create_table('toppings_foods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topping_id', sa.Integer(), nullable=False, comment='идентификатор Ингредиенты'),
    sa.Column('food_id', sa.Integer(), nullable=False, comment='идентификатор Блюдо'),
    sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['topping_id'], ['toppings.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_toppings_foods_food_id'), 'toppings_foods', ['food_id'], unique=False)
    op.create_index(op.f('ix_toppings_foods_id'), 'toppings_foods', ['id'], unique=True)
    op.create_index(op.f('ix_toppings_foods_topping_id'), 'toppings_foods', ['topping_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_toppings_foods_topping_id'), table_name='toppings_foods')
    op.drop_index(op.f('ix_toppings_foods_id'), table_name='toppings_foods')
    op.drop_index(op.f('ix_toppings_foods_food_id'), table_name='toppings_foods')
    op.drop_table('toppings_foods')
    op.drop_index(op.f('ix_foods_name'), table_name='foods')
    op.drop_index(op.f('ix_foods_id'), table_name='foods')
    op.drop_index(op.f('ix_foods_description'), table_name='foods')
    op.drop_index(op.f('ix_foods_category_id'), table_name='foods')
    op.drop_table('foods')
    op.drop_index(op.f('ix_toppings_name'), table_name='toppings')
    op.drop_index(op.f('ix_toppings_id'), table_name='toppings')
    op.drop_table('toppings')
    op.drop_index(op.f('ix_food_categories_name'), table_name='food_categories')
    op.drop_index(op.f('ix_food_categories_id'), table_name='food_categories')
    op.drop_table('food_categories')
    # ### end Alembic commands ###
