package com.projecte_final.mysong.models;

import jakarta.persistence.*;
import lombok.Data;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

@Data
@Entity
@Table(name = "canciones")
public class Cancion {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String nombre;
    
    private String artista;
    
    private String album;
    
    @Lob
    @Column(name = "data")
    @JsonIgnore
    private byte[] data;  // Almacena los bytes del archivo de audio
    
    @Column(name="archivo_mp3")
    private String nombreArchivo; 
    
    private Integer likes;
    
    // Relación ManyToOne con el usuario que subió la canción
    @ManyToOne
    @JoinColumn(name = "usuario_id", referencedColumnName = "id")
    private Usuario usuario;
    
    @ManyToMany(mappedBy = "canciones")
    private List<ListaReproduccion> listasReproduccion;
    
    // Getters y Setters
}
