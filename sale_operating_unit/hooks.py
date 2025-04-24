def pre_init_hook(cr):
    """Set OU for existing (posted) sales orders to prevent errors by the constraint"""
    cr.execute(
        """
        ALTER TABLE sale_order
        ADD COLUMN IF NOT EXISTS operating_unit_id INTEGER;
        """
    )
    cr.execute(
        """
        UPDATE sale_order so
        SET operating_unit_id = team.operating_unit_id
        FROM crm_team team
        WHERE so.team_id = team.id
        AND so.operating_unit_id IS NULL
        AND so.team_id IS NOT NULL
        """
    )
