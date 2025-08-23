package com.PL.premier_hub.player;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PlayerRepository extends JpaRepository<Player, String> {
    void deleteByName(String playerName);
    Optional<Player> findByName(String playerName);
}
