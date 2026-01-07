"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-01-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables for the nutritionist menu planner platform."""

    # ============================================
    # 1. 사용자 관리 (User Management)
    # ============================================

    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('organization', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_login_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_is_active', 'users', ['is_active'])

    # ============================================
    # 2. 식단 관리 (Meal Plan Management)
    # ============================================

    op.create_table(
        'meal_plans',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('target_count', sa.Integer(), nullable=False),
        sa.Column('budget_per_person', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('total_budget', sa.DECIMAL(12, 2), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('confirmed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('published_at', sa.TIMESTAMP(), nullable=True),
        sa.CheckConstraint('month >= 1 AND month <= 12', name='ck_meal_plans_month'),
        sa.CheckConstraint('target_count > 0', name='ck_meal_plans_target_count'),
        sa.CheckConstraint('budget_per_person >= 0', name='ck_meal_plans_budget_per_person'),
        sa.CheckConstraint("status IN ('draft', 'confirmed', 'published')", name='ck_meal_plans_status'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'year', 'month', name='uq_meal_plans_user_year_month')
    )
    op.create_index('ix_meal_plans_user_status', 'meal_plans', ['user_id', 'status'])
    op.create_index('ix_meal_plans_created_at', 'meal_plans', ['created_at'])

    op.create_table(
        'daily_meals',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('meal_plan_id', sa.BigInteger(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('day_of_week', sa.String(10), nullable=False),
        sa.Column('is_holiday', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('holiday_name', sa.String(100), nullable=True),
        sa.Column('total_calories', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('total_price_per_person', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('meal_plan_id', 'date', name='uq_daily_meals_plan_date')
    )
    op.create_index('ix_daily_meals_date', 'daily_meals', ['date'])

    op.create_table(
        'meal_items',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('daily_meal_id', sa.BigInteger(), nullable=False),
        sa.Column('category', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('serving_size_g', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('price_per_person', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('calories', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('cooking_method', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint('serving_size_g > 0', name='ck_meal_items_serving_size'),
        sa.CheckConstraint('price_per_person >= 0', name='ck_meal_items_price'),
        sa.CheckConstraint("category IN ('rice', 'soup', 'side_dish', 'dessert')", name='ck_meal_items_category'),
        sa.ForeignKeyConstraint(['daily_meal_id'], ['daily_meals.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_meal_items_daily_meal_category_order', 'meal_items',
                    ['daily_meal_id', 'category', 'display_order'])

    # ============================================
    # 3. 식재료 관리 (Ingredient Management)
    # ============================================

    op.create_table(
        'ingredients',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('name_normalized', sa.String(255), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('unit', sa.String(20), nullable=False),
        sa.Column('is_seasonal', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('seasonal_months', sa.String(50), nullable=True),
        sa.Column('supply_stability', sa.String(20), nullable=False, server_default='stable'),
        sa.Column('origin', sa.String(100), nullable=True),
        sa.Column('storage_method', sa.String(100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint(
            "category IN ('vegetable', 'meat', 'seafood', 'grain', 'dairy', 'seasoning', 'processed', 'other')",
            name='ck_ingredients_category'
        ),
        sa.CheckConstraint(
            "unit IN ('g', 'kg', 'ml', 'l', 'ea')",
            name='ck_ingredients_unit'
        ),
        sa.CheckConstraint(
            "supply_stability IN ('stable', 'unstable', 'seasonal')",
            name='ck_ingredients_supply_stability'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_ingredients_name', 'ingredients', ['name'], unique=True)
    op.create_index('ix_ingredients_name_normalized', 'ingredients', ['name_normalized'])
    op.create_index('ix_ingredients_category', 'ingredients', ['category'])

    op.create_table(
        'meal_item_ingredients',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('meal_item_id', sa.BigInteger(), nullable=False),
        sa.Column('ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('quantity_g', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint('quantity_g > 0', name='ck_meal_item_ingredients_quantity'),
        sa.ForeignKeyConstraint(['meal_item_id'], ['meal_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('meal_item_id', 'ingredient_id', name='uq_meal_item_ingredients')
    )

    op.create_table(
        'ingredient_substitutes',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('substitute_ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('substitution_ratio', sa.DECIMAL(5, 2), nullable=False, server_default='1.0'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint('substitution_ratio > 0', name='ck_ingredient_substitutes_ratio'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['substitute_ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ingredient_id', 'substitute_ingredient_id', name='uq_ingredient_substitutes')
    )

    op.create_table(
        'suppliers',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('contact_person', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('business_number', sa.String(20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_suppliers_is_active', 'suppliers', ['is_active'])

    op.create_table(
        'supplier_items',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('supplier_id', sa.BigInteger(), nullable=False),
        sa.Column('ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('price_per_unit', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('unit_size', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('availability_status', sa.String(20), nullable=False, server_default='available'),
        sa.Column('min_order_quantity', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('delivery_days', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint(
            "availability_status IN ('available', 'out_of_stock', 'discontinued')",
            name='ck_supplier_items_availability'
        ),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('supplier_id', 'ingredient_id', name='uq_supplier_items')
    )
    op.create_index('ix_supplier_items_availability', 'supplier_items', ['availability_status'])

    # ============================================
    # 4. 영양 정보 (Nutrition Information)
    # ============================================

    op.create_table(
        'nutrition_info',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('serving_size_g', sa.DECIMAL(8, 2), nullable=False, server_default='100'),
        sa.Column('calories_kcal', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('carbohydrate_g', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('protein_g', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('fat_g', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('sodium_mg', sa.DECIMAL(8, 2), nullable=False),
        sa.Column('sugar_g', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('saturated_fat_g', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('cholesterol_mg', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('dietary_fiber_g', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('calcium_mg', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('iron_mg', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('vitamin_a_ug', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('vitamin_c_mg', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('data_source', sa.String(100), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint('serving_size_g > 0', name='ck_nutrition_info_serving_size'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ingredient_id')
    )
    op.create_index('ix_nutrition_info_ingredient', 'nutrition_info', ['ingredient_id'], unique=True)

    # ============================================
    # 5. 알레르기 관리 (Allergen Management)
    # ============================================

    op.create_table(
        'allergens',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('name_en', sa.String(100), nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_mandatory_label', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint(
            "category IN ('food_allergy', 'religious', 'cultural')",
            name='ck_allergens_category'
        ),
        sa.CheckConstraint(
            "severity IN ('high', 'medium', 'low')",
            name='ck_allergens_severity'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_allergens_name', 'allergens', ['name'], unique=True)
    op.create_index('ix_allergens_category', 'allergens', ['category'])

    op.create_table(
        'ingredient_allergens',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ingredient_id', sa.BigInteger(), nullable=False),
        sa.Column('allergen_id', sa.BigInteger(), nullable=False),
        sa.Column('contamination_level', sa.String(20), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint(
            "contamination_level IN ('contains', 'may_contain', 'traces')",
            name='ck_ingredient_allergens_contamination'
        ),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['allergen_id'], ['allergens.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ingredient_id', 'allergen_id', name='uq_ingredient_allergens')
    )
    op.create_index('ix_ingredient_allergens_allergen', 'ingredient_allergens', ['allergen_id'])

    # ============================================
    # 6. 이력 관리 (History Management)
    # ============================================

    op.create_table(
        'meal_plan_history',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('meal_plan_id', sa.BigInteger(), nullable=False),
        sa.Column('meal_item_id', sa.BigInteger(), nullable=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('changed_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('before_value', postgresql.JSONB(), nullable=True),
        sa.Column('after_value', postgresql.JSONB(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['meal_item_id'], ['meal_items.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_meal_plan_history_meal_plan', 'meal_plan_history', ['meal_plan_id'])
    op.create_index('ix_meal_plan_history_meal_plan_changed', 'meal_plan_history',
                    ['meal_plan_id', 'changed_at'])
    op.create_index('ix_meal_plan_history_user', 'meal_plan_history', ['user_id'])

    # ============================================
    # 7. 사용자 활동 추적 (User Activity Tracking)
    # ============================================

    op.create_table(
        'user_activity_log',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('activity_type', sa.String(50), nullable=False),
        sa.Column('activity_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_activity_log_user', 'user_activity_log', ['user_id'])
    op.create_index('ix_user_activity_log_activity_at', 'user_activity_log', ['activity_at'])
    op.create_index('ix_user_activity_log_activity_type', 'user_activity_log', ['activity_type'])

    op.create_table(
        'user_favorites',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('item_id', sa.BigInteger(), nullable=False),
        sa.Column('added_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.Column('usage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'item_type', 'item_id', name='uq_user_favorites')
    )
    op.create_index('ix_user_favorites_user', 'user_favorites', ['user_id'])

    # ============================================
    # 8. KPI 집계 테이블 (KPI Aggregation)
    # ============================================

    op.create_table(
        'monthly_active_users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('year_month', sa.Date(), nullable=False),
        sa.Column('total_active_users', sa.Integer(), nullable=False),
        sa.Column('new_users', sa.Integer(), nullable=False),
        sa.Column('returning_users', sa.Integer(), nullable=False),
        sa.Column('churned_users', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('year_month')
    )
    op.create_index('ix_monthly_active_users_year_month', 'monthly_active_users',
                    ['year_month'], unique=True)

    op.create_table(
        'meal_plan_time_tracking',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('meal_plan_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('started_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('generated_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('confirmed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('total_edit_time_seconds', sa.Integer(), nullable=True),
        sa.Column('baseline_time_hours', sa.DECIMAL(5, 2), nullable=True),
        sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('meal_plan_id')
    )
    op.create_index('ix_meal_plan_time_tracking_meal_plan', 'meal_plan_time_tracking',
                    ['meal_plan_id'], unique=True)
    op.create_index('ix_meal_plan_time_tracking_user', 'meal_plan_time_tracking', ['user_id'])

    op.create_table(
        'meal_plan_reuse_tracking',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('meal_plan_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('reuse_type', sa.String(50), nullable=False),
        sa.Column('source_meal_plan_id', sa.BigInteger(), nullable=True),
        sa.Column('source_item_id', sa.BigInteger(), nullable=True),
        sa.Column('reused_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_meal_plan_id'], ['meal_plans.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_meal_plan_reuse_tracking_meal_plan', 'meal_plan_reuse_tracking',
                    ['meal_plan_id'])
    op.create_index('ix_meal_plan_reuse_tracking_user', 'meal_plan_reuse_tracking', ['user_id'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('meal_plan_reuse_tracking')
    op.drop_table('meal_plan_time_tracking')
    op.drop_table('monthly_active_users')
    op.drop_table('user_favorites')
    op.drop_table('user_activity_log')
    op.drop_table('meal_plan_history')
    op.drop_table('ingredient_allergens')
    op.drop_table('allergens')
    op.drop_table('nutrition_info')
    op.drop_table('supplier_items')
    op.drop_table('suppliers')
    op.drop_table('ingredient_substitutes')
    op.drop_table('meal_item_ingredients')
    op.drop_table('ingredients')
    op.drop_table('meal_items')
    op.drop_table('daily_meals')
    op.drop_table('meal_plans')
    op.drop_table('users')
