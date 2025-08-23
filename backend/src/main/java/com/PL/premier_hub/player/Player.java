package com.PL.premier_hub.player;


import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "player_stats")
public class Player {
    @Id
    @Column(name = "player_name", unique = true)
    private String name;
    private String nation;
    private String position;
    private Double age;
    private Integer matches_played;
    private Double minutes_played;
    private Double goals;
    private Double assists;
    private Double penalty_kicks;
    private Double yellow_cards;
    private Double red_cards;
    private String team;

    public Player() {
    }

    public Player(String name, String nation, String position, Double age, Integer matches_played, Double minutes_played, Double goals, Double assists, Double penalty_kicks, Double yellow_cards, Double red_cards, String team) {
        this.name = name;
        this.nation = nation;
        this.position = position;
        this.age = age;
        this.matches_played = matches_played;
        this.minutes_played = minutes_played;
        this.goals = goals;
        this.assists = assists;
        this.penalty_kicks = penalty_kicks;
        this.yellow_cards = yellow_cards;
        this.red_cards = red_cards;
        this.team = team;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getNation() {
        return nation;
    }

    public void setNation(String nation) {
        this.nation = nation;
    }

    public String getPosition() {
        return position;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    public Double getAge() {
        return age;
    }

    public void setAge(Double age) {
        this.age = age;
    }

    public Integer getMatches_played() {
        return matches_played;
    }

    public void setMatches_played(Integer matches_played) {
        this.matches_played = matches_played;
    }

    public Double getMinutes_played() {
        return minutes_played;
    }

    public void setMinutes_played(Double minutes_played) {
        this.minutes_played = minutes_played;
    }

    public Double getGoals() {
        return goals;
    }

    public void setGoals(Double goals) {
        this.goals = goals;
    }

    public Double getAssists() {
        return assists;
    }

    public void setAssists(Double assists) {
        this.assists = assists;
    }

    public Double getPenalty_kicks() {
        return penalty_kicks;
    }

    public void setPenalty_kicks(Double penalty_kicks) {
        this.penalty_kicks = penalty_kicks;
    }

    public Double getYellow_cards() {
        return yellow_cards;
    }

    public void setYellow_cards(Double yellow_cards) {
        this.yellow_cards = yellow_cards;
    }

    public Double getRed_cards() {
        return red_cards;
    }

    public void setRed_cards(Double red_cards) {
        this.red_cards = red_cards;
    }

    public String getTeam() {
        return team;
    }

    public void setTeam(String team) {
        this.team = team;
    }
}
