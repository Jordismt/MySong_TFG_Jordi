package com.projecte_final.mysong.modelsDTO;

import lombok.Data;

@Data
public class CancionDTO {
    private Long id;
    private String nombre;
    private String artista;
    private String album;
    private String nombreArchivo;
    private Integer likes;
    private String usuarioNombre;

    // Getters y Setters
}

