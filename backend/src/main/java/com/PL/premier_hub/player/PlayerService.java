package com.PL.premier_hub.player;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class PlayerService {
    private final PlayerRepository playerRepository;
    @Autowired
    public PlayerService(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    public List<Player> getPlayers(){
        return playerRepository.findAll();
    }

    public List<Player> getPlayersByTeam(String teamName){
        return playerRepository.findAll().stream()
                .filter(player -> teamName.equals(player.getTeam()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByName(String searchText){
        return playerRepository.findAll().stream().filter(player -> player.getName()
                .toLowerCase().contains(searchText.toLowerCase()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByPosition(String searchText){
        return playerRepository.findAll().stream().filter(player -> player.getPosition()
                .toLowerCase().contains(searchText)).collect(Collectors.toList());
    }

    public List<Player> getPlayersByNation(String searchText){
        return playerRepository.findAll().stream().filter(player -> player.getNation().toLowerCase()
                .contains(searchText.toLowerCase())).collect(Collectors.toList());
    }

    public List<Player> getPlayersByTeamAndPosition(String teamName, String position){
        return playerRepository.findAll().stream().filter(player ->
                teamName.equals(player.getTeam()) && position.equals(player.getPosition()))
                .collect(Collectors.toList());
    }
}
