package com.projecte_final.mysong.models;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import lombok.Data;

import java.util.List;

@Data
@Entity
@Table(name = "usuarios")
public class Usuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nombre;

    @Column(name = "correo_electronico")
    private String correoElectronico;

    private String contraseña;

    @Column(name = "tipo_usuario")
    private String tipoUsuario;

    @OneToMany(mappedBy = "usuario")
    @JsonManagedReference
    private List<ListaReproduccion> listasReproduccion;
}
