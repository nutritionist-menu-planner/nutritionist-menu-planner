"""Seed allergen data (MFDS 21 allergens)

Revision ID: 002
Revises: 001
Create Date: 2026-01-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Insert 21 allergens from MFDS (Ministry of Food and Drug Safety)."""

    # Bind the connection
    conn = op.get_bind()

    # Insert allergen data
    allergens_data = [
        # High severity allergens
        ('난류(계란)', 'Eggs', 'food_allergy', 'high', '달걀 및 이를 함유한 제품', True),
        ('우유', 'Milk', 'food_allergy', 'high', '우유 및 유제품', True),
        ('메밀', 'Buckwheat', 'food_allergy', 'high', '메밀 및 이를 함유한 제품', True),
        ('땅콩', 'Peanuts', 'food_allergy', 'high', '땅콩 및 이를 함유한 제품', True),
        ('밀', 'Wheat', 'food_allergy', 'high', '밀 및 이를 함유한 제품', True),
        ('게', 'Crab', 'food_allergy', 'high', '게 및 이를 함유한 제품', True),
        ('새우', 'Shrimp', 'food_allergy', 'high', '새우 및 이를 함유한 제품', True),
        ('아황산류', 'Sulfites', 'food_allergy', 'high', '아황산류 함유 식품 (1kg당 10mg 이상)', True),
        ('호두', 'Walnut', 'food_allergy', 'high', '호두 및 이를 함유한 제품', True),
        ('조개류', 'Shellfish', 'food_allergy', 'high', '조개류 (굴, 전복, 홍합 포함)', True),

        # Medium severity allergens
        ('대두', 'Soybeans', 'food_allergy', 'medium', '대두 및 이를 함유한 제품', True),
        ('고등어', 'Mackerel', 'food_allergy', 'medium', '고등어 및 이를 함유한 제품', True),
        ('돼지고기', 'Pork', 'food_allergy', 'medium', '돼지고기 및 이를 함유한 제품', True),
        ('복숭아', 'Peach', 'food_allergy', 'medium', '복숭아 및 이를 함유한 제품', True),
        ('닭고기', 'Chicken', 'food_allergy', 'medium', '닭고기 및 이를 함유한 제품', True),
        ('쇠고기', 'Beef', 'food_allergy', 'medium', '쇠고기 및 이를 함유한 제품', True),
        ('오징어', 'Squid', 'food_allergy', 'medium', '오징어 및 이를 함유한 제품', True),
        ('잣', 'Pine Nuts', 'food_allergy', 'medium', '잣 및 이를 함유한 제품', True),

        # Low severity allergens
        ('토마토', 'Tomato', 'food_allergy', 'low', '토마토 및 이를 함유한 제품', True),
        ('밤', 'Chestnut', 'food_allergy', 'low', '밤 및 이를 함유한 제품', True),
        ('알류', 'Nuts (General)', 'food_allergy', 'medium', '견과류 전반 (호두, 땅콩 제외)', True),
    ]

    # Execute insert
    for name, name_en, category, severity, description, is_mandatory in allergens_data:
        conn.execute(
            sa.text(
                """
                INSERT INTO allergens (name, name_en, category, severity, description, is_mandatory_label)
                VALUES (:name, :name_en, :category, :severity, :description, :is_mandatory)
                """
            ),
            {
                'name': name,
                'name_en': name_en,
                'category': category,
                'severity': severity,
                'description': description,
                'is_mandatory': is_mandatory
            }
        )


def downgrade() -> None:
    """Remove allergen seed data."""
    op.execute("DELETE FROM allergens WHERE is_mandatory_label = true")
