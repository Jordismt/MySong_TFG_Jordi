package com.projecte_final.mysong.models;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;

import lombok.Data;

import java.util.List;

@Data
@Entity
@Table(name = "listas_reproduccion")
public class ListaReproduccion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "id_usuario", nullable = false)
    private Long idUsuario;

    private String nombre;
    @Column(name = "nombre_usuario")
    private String nombreUsuario;
    @ManyToOne
    @JoinColumn(name = "id_usuario", referencedColumnName = "id", insertable = false, updatable = false)
    @JsonBackReference
    private Usuario usuario;

    @ManyToMany
    @JoinTable(
            name = "canciones_en_lista",
            joinColumns = @JoinColumn(name = "id_lista"),
            inverseJoinColumns = @JoinColumn(name = "id_cancion")
    )
    @JsonIgnore
    private List<Cancion> canciones;
}
