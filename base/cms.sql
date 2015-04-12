SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `cms` ;
CREATE SCHEMA IF NOT EXISTS `cms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `cms` ;

-- -----------------------------------------------------
-- Table `cms`.`Cms`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`Cms` ;

CREATE  TABLE IF NOT EXISTS `cms`.`Cms` (
  `idCms` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Descripcion` VARCHAR(150) NOT NULL ,
  `Imagen` VARCHAR(45) NOT NULL ,
  `Activo` TINYINT(1) NOT NULL ,
  `estilos` VARCHAR(150) NOT NULL ,
  `contenido` VARCHAR(150) NULL ,
  PRIMARY KEY (`idCms`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`Conjunto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`Conjunto` ;

CREATE  TABLE IF NOT EXISTS `cms`.`Conjunto` (
  `idConjunto` INT NOT NULL AUTO_INCREMENT ,
  `Tienda` INT NOT NULL ,
  `fecha` DATE NULL ,
  `Activo` TINYINT(1) NULL ,
  `Cms` INT NOT NULL ,
  PRIMARY KEY (`idConjunto`) ,
  INDEX `fk_Conjunto_Cms_idx` (`Cms` ASC) ,
  CONSTRAINT `fk_Conjunto_Cms`
    FOREIGN KEY (`Cms` )
    REFERENCES `cms`.`Cms` (`idCms` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`Secciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`Secciones` ;

CREATE  TABLE IF NOT EXISTS `cms`.`Secciones` (
  `idSecciones` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NOT NULL ,
  `Titulo` VARCHAR(45) NOT NULL ,
  `contenido` VARCHAR(250) NOT NULL ,
  `Activo` TINYINT(1) NULL ,
  `Conjunto` INT NOT NULL ,
  PRIMARY KEY (`idSecciones`) ,
  INDEX `fk_Secciones_Conjunto1_idx` (`Conjunto` ASC) ,
  CONSTRAINT `fk_Secciones_Conjunto1`
    FOREIGN KEY (`Conjunto` )
    REFERENCES `cms`.`Conjunto` (`idConjunto` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`subsecciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`subsecciones` ;

CREATE  TABLE IF NOT EXISTS `cms`.`subsecciones` (
  `idsubsecciones` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NULL ,
  `Titulo` VARCHAR(45) NULL ,
  `Contenido` TEXT NULL ,
  `Secciones` INT NOT NULL ,
  PRIMARY KEY (`idsubsecciones`) ,
  INDEX `fk_subsecciones_Secciones1_idx` (`Secciones` ASC) ,
  CONSTRAINT `fk_subsecciones_Secciones1`
    FOREIGN KEY (`Secciones` )
    REFERENCES `cms`.`Secciones` (`idSecciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`Imagenes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`Imagenes` ;

CREATE  TABLE IF NOT EXISTS `cms`.`Imagenes` (
  `idImagenes` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NULL ,
  `Archivo` VARCHAR(150) NULL ,
  `Tipo` VARCHAR(45) NULL ,
  `Activo` TINYINT(1) NULL ,
  PRIMARY KEY (`idImagenes`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`GaleriaCms`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`GaleriaCms` ;

CREATE  TABLE IF NOT EXISTS `cms`.`GaleriaCms` (
  `idGaleria` INT NOT NULL ,
  `Nombre` VARCHAR(45) NULL ,
  `Activo` TINYINT(1) NULL ,
  `subsecciones` INT NOT NULL ,
  PRIMARY KEY (`idGaleria`) ,
  INDEX `fk_Galeria_subsecciones1_idx` (`subsecciones` ASC) ,
  CONSTRAINT `fk_Galeria_subsecciones1`
    FOREIGN KEY (`subsecciones` )
    REFERENCES `cms`.`subsecciones` (`idsubsecciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`Galeria_Imagenes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`Galeria_Imagenes` ;

CREATE  TABLE IF NOT EXISTS `cms`.`Galeria_Imagenes` (
  `Galeria` INT NOT NULL ,
  `Imagenes` INT NOT NULL ,
  `Activo` TINYINT(1) NULL ,
  PRIMARY KEY (`Galeria`, `Imagenes`) ,
  INDEX `fk_Galeria_has_Imagenes_Imagenes1_idx` (`Imagenes` ASC) ,
  INDEX `fk_Galeria_has_Imagenes_Galeria1_idx` (`Galeria` ASC) ,
  CONSTRAINT `fk_Galeria_has_Imagenes_Galeria1`
    FOREIGN KEY (`Galeria` )
    REFERENCES `cms`.`GaleriaCms` (`idGaleria` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Galeria_has_Imagenes_Imagenes1`
    FOREIGN KEY (`Imagenes` )
    REFERENCES `cms`.`Imagenes` (`idImagenes` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`PlugIn`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`PlugIn` ;

CREATE  TABLE IF NOT EXISTS `cms`.`PlugIn` (
  `idPlugIn` INT NOT NULL AUTO_INCREMENT ,
  `Nombre` VARCHAR(45) NULL ,
  `Tipo` VARCHAR(45) NULL ,
  `Archivo` VARCHAR(45) NULL ,
  PRIMARY KEY (`idPlugIn`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`subsecciones_PlugIn`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`subsecciones_PlugIn` ;

CREATE  TABLE IF NOT EXISTS `cms`.`subsecciones_PlugIn` (
  `subsecciones` INT NOT NULL ,
  `PlugIn` INT NOT NULL ,
  PRIMARY KEY (`subsecciones`, `PlugIn`) ,
  INDEX `fk_subsecciones_has_PlugIn_PlugIn1_idx` (`PlugIn` ASC) ,
  INDEX `fk_subsecciones_has_PlugIn_subsecciones1_idx` (`subsecciones` ASC) ,
  CONSTRAINT `fk_subsecciones_has_PlugIn_subsecciones1`
    FOREIGN KEY (`subsecciones` )
    REFERENCES `cms`.`subsecciones` (`idsubsecciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_subsecciones_has_PlugIn_PlugIn1`
    FOREIGN KEY (`PlugIn` )
    REFERENCES `cms`.`PlugIn` (`idPlugIn` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`propiedades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`propiedades` ;

CREATE  TABLE IF NOT EXISTS `cms`.`propiedades` (
  `idpropiedades` INT NOT NULL AUTO_INCREMENT ,
  `nombre` VARCHAR(45) NULL ,
  `valor` VARCHAR(100) NULL ,
  `Secciones` INT NOT NULL ,
  PRIMARY KEY (`idpropiedades`) ,
  INDEX `fk_propiedades_Secciones1_idx` (`Secciones` ASC) ,
  CONSTRAINT `fk_propiedades_Secciones1`
    FOREIGN KEY (`Secciones` )
    REFERENCES `cms`.`Secciones` (`idSecciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `cms`.`PropiedadesSubsecciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cms`.`PropiedadesSubsecciones` ;

CREATE  TABLE IF NOT EXISTS `cms`.`PropiedadesSubsecciones` (
  `id` INT NOT NULL ,
  `nombre` VARCHAR(45) NULL ,
  `Valor` VARCHAR(45) NULL ,
  `PropiedadesSubseccionescol` VARCHAR(45) NULL ,
  `subsecciones` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_PropiedadesSubsecciones_subsecciones1_idx` (`subsecciones` ASC) ,
  CONSTRAINT `fk_PropiedadesSubsecciones_subsecciones1`
    FOREIGN KEY (`subsecciones` )
    REFERENCES `cms`.`subsecciones` (`idsubsecciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `cms` ;

-- -----------------------------------------------------
-- Placeholder table for view `cms`.`view1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cms`.`view1` (`id` INT);

-- -----------------------------------------------------
-- View `cms`.`view1`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `cms`.`view1` ;
DROP TABLE IF EXISTS `cms`.`view1`;
USE `cms`;
;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
