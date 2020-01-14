from __future__ import annotations

import uuid

from pluribus.game.player import Player


class Pot:
    """Class to manage the bets from all players."""

    def __init__(self):
        """Construct the pot, and initialise the counter."""
        self._side_pot = {}
        self._side_pots = []
        self._uid = str(uuid.uuid4().hex)
        self.reset()

    def __repr__(self):
        """Nicer way to print a Pot object."""
        return f"<Pot n_chips={self.total}>"

    def __getitem__(self, player: Player):
        """Get a players contribution to the pot."""
        if not isinstance(player, Player):
            raise ValueError(
                f'Index the pot with the player to get the contribution.')
        return sum(
            pot.get(player, 0) for pot in self._side_pots + [self._side_pot]
        )

    def reset(self):
        """Reset the pot."""
        self._side_pot = {}
        self._side_pots = []

    def add_chips(self, player: Player, n_chips: int):
        """Add chips to the pot, from a player for a given round."""
        if n_chips < 0:
            raise ValueError(f'Negative chips cannot be added to the pot.')
        if player in self._side_pot:
            # We have already bet with this player, make a new side pot.
            self._side_pots.append({k: v for k, v in self._side_pot.items()})
            self._side_pot = {}
            self._side_pot[player] = n_chips
        elif all(c == n_chips for c in self._side_pot.values()):
            # All the other players bets are equal to this bet, so add to
            # current side pot.
            self._side_pot[player] = n_chips
        else:
            # Else player is not in the current side pot, and the amount is
            # different to the side current values in the side pot.
            original_n_chips = list(self._side_pot.values())[0]
            original_players = list(self._side_pot.keys())
            smallest_n_chips = min(original_n_chips, n_chips)
            self._side_pot[player] = smallest_n_chips
            self._side_pots.append({
                p: smallest_n_chips for p in original_players + [player]
            })
            n_chips_diff = abs(original_n_chips - n_chips)
            if original_n_chips > n_chips:
                diff_players = original_players
            else:
                diff_players = [player]
            self._side_pot = {p: n_chips_diff for p in diff_players}

    @property
    def uid(self):
        """Get a unique identifier for this pot."""
        return self._uid

    @property
    def total(self):
        """Return the total in the pot from all players."""
        return sum(sum(p.values()) for p in self._side_pots + [self._side_pot])
