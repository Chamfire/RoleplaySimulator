import sqlite3

class CrearTablas:
    def __init__(self):
        #Creamos las tablas para la bbdd
        conn = sqlite3.connect("simuladordnd.db") #creamos la base de datos si es que no existe ya con ese nombre

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugador (
                id_jugador text PRIMARY KEY,
                pic integer NOT NULL CONSTRAINT pic_no_valido CHECK(pic >=0 AND pic <=6),
                name text NOT NULL,
                is_my_id boolean NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partida(
                server_code text NOT NULL,
                numPartida text PRIMARY KEY,
                ultima_conexion text,
                horas_jugadas integer NOT NULL CONSTRAINT horas_negativas CHECK(horas_jugadas >= 0),
                ubicacion_historia text NOT NULL,
                num_jugadores integer NOT NULL CONSTRAINT num_jugadores_erroneo CHECK(num_jugadores > 0 AND num_jugadores <=6),
                nombre text UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mapageneral (
                partida_id text REFERENCES partida(numPartida) PRIMARY KEY,
                size text NOT NULL,
                directorio_imagen text NOT NULL,
                matriz_codificacion text NOT NULL
            )
        """)

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_mapa_general
                BEFORE DELETE ON partida
                    BEGIN
                        DELETE FROM mapageneral
                        WHERE partida_id = OLD.numPartida;
                    END;
        """
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ubicacion (
                partida_id_mapa text NOT NULL REFERENCES mapageneral(numPartida),
                nombre text NOT NULL,
                es_fin boolean NOT NULL,
                matriz_codificacion text NOT NULL,
                directorio_imagen text NOT NULL,
                es_inicio boolean NOT NULL,
                es_punto_clave boolean NOT NULL,
                coordenadas_esquina_izqda_sup text NOT NULL,
                size text NOT NULL,
                UNIQUE(coordenadas_esquina_izqda_sup,size),
                PRIMARY KEY(partida_id_mapa,nombre)
            )
        """)

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_ubicacion
                BEFORE DELETE ON partida
                    BEGIN
                        DELETE FROM ubicacion
                        WHERE partida_id_mapa = OLD.numPartida;
                    END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quest (
                partida_id text REFERENCES partida(numPartida) NOT NULL,
                num_quest integer UNIQUE NOT NULL CHECK(num_quest >=0),
                estado_quest text REFERENCES enum_estado(estado_quest) NOT NULL,
                num_npc_partida_q integer,
                partida_id_npc text CONSTRAINT different_ids_npc_and_id CHECK(partida_id == partida_id_npc),
                FOREIGN KEY(num_npc_partida_q,partida_id_npc) REFERENCES npc(num_npc_partida,id_partida) ON DELETE CASCADE,
                PRIMARY KEY(partida_id,num_quest)
            )
        """)

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_quest
                BEFORE DELETE ON partida
                    BEGIN
                        DELETE FROM quest
                        WHERE partida_id = OLD.numPartida;
                    END;
        """
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_estado (
                estado_quest text PRIMARY KEY 
            )
        """)
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_quest
                BEFORE DELETE ON enum_estado
                    BEGIN
                        DELETE FROM quest
                        WHERE estado_quest = OLD.estado_quest;
                    END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variable_chequeo (
                valor text,
                partida_id_c text UNIQUE NOT NULL,
                num_quest_c integer UNIQUE NOT NULL,
                tipo_var text NOT NULL,
                npartida integer UNIQUE NOT NULL CONSTRAINT npartida_less_than_zero_or_equal CHECK(npartida >0),
                FOREIGN KEY(partida_id_c,num_quest_c) REFERENCES quest(partida_id,num_quest) ON DELETE CASCADE,
                PRIMARY KEY(npartida,partida_id_c,num_quest_c)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS npc (
                num_npc_partida integer UNIQUE NOT NULL CONSTRAINT num_npc_partida_less_than_zero CHECK(num_npc_partida >=0),
                partida_id text REFERENCES partida(numPartida) NOT NULL,
                PRIMARY KEY(num_npc_partida,partida_id)
            )
        """)

        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_npc
                BEFORE DELETE ON partida
                    BEGIN
                        DELETE FROM npc
                        WHERE partida_id = OLD.numPartida;
                    END;
        """
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dialogo (
                num_dialogo integer UNIQUE NOT NULL CONSTRAINT num_dialogo_less_than_zero_or_equal CHECK(num_dialogo >0),
                texto text NOT NULL,
                num_npc_partida_d integer UNIQUE NOT NULL,
                partida_id text UNIQUE NOT NULL,
                FOREIGN KEY(num_npc_partida_d,partida_id) REFERENCES npc(num_npc_partida,partida_id) ON DELETE CASCADE,
                PRIMARY KEY(num_dialogo,num_npc_partida_d,partida_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_trasfondo (
                tipo_trasfondo text PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vinculos (
                num_id integer PRIMARY KEY CHECK(num_id >0),
                vinculo text NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS defectos (
                num_id integer PRIMARY KEY CHECK(num_id >0),
                defecto text NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ideales (
                num_id integer PRIMARY KEY CHECK(num_id >0),
                ideal text NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rasgos_personalidad (
                num_id integer PRIMARY KEY CHECK(num_id >0),
                rasgo_personalidad text NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trasfondo (
                tipo_trasfondo text NOT NULL REFERENCES enum_trasfondo(tipo_trasfondo) ON DELETE CASCADE,
                vinculo text NOT NULL REFERENCES vinculos(vinculo) ON UPDATE CASCADE ON DELETE CASCADE,
                defecto text NOT NULL REFERENCES defectos(defecto) ON UPDATE CASCADE ON DELETE CASCADE,
                ideal text NOT NULL REFERENCES ideales(ideal) ON UPDATE CASCADE ON DELETE CASCADE,
                rasgo_personalidad text NOT NULL REFERENCES rasgos_personalidad(rasgo_personalidad) ON UPDATE CASCADE ON DELETE CASCADE,
                num_trasfondo integer PRIMARY KEY CONSTRAINT num_trasfondo_less_or_equal_than_zero CHECK(num_trasfondo >0)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_raza (
                tipo_raza text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_clase (
                tipo_clase text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_alineamiento (
                tipo_alineamiento text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partida_jugador (
                nMuertes_partida integer NOT NULL CONSTRAINT nMuertes_less_than_zero CHECK(nMuertes_partida >=0),
                partida_id text NOT NULL REFERENCES partida(numPartida),
                id_jugador text NOT NULL REFERENCES jugador(id_jugador),
                PRIMARY KEY(partida_id,id_jugador)
            )        
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador
                BEFORE UPDATE OF id_jugador ON jugador
                WHEN EXISTS (SELECT 1 FROM partida_jugador WHERE id_jugador = OLD.id_jugador)
                AND EXISTS (SELECT 1 FROM partida_jugador)
                    BEGIN
                        UPDATE partida_jugador
                        SET id_jugador = NEW.id_jugador
                        WHERE id_jugador = OLD.id_jugador;
                    END;
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS eliminar_partida_jugador
                BEFORE DELETE ON partida
                    BEGIN
                        DELETE FROM partida_jugador
                        WHERE partida_id = OLD.numPartida;
                    END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS size (
                tipo_size text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personaje (
                name text NOT NULL,
                sm1 boolean NOT NULL,
                sm2 boolean NOT NULL,
                sm3 boolean NOT NULL,
                nivel integer NOT NULL CONSTRAINT not_a_real_level CHECK(nivel >=0 and nivel <=20),
                inspiracion integer NOT NULL CONSTRAINT inspiracion_less_than_zero CHECK(inspiracion >=0),
                esta_muerto boolean NOT NULL CONSTRAINT missmatch_esta_muerto_and_sms CHECK((esta_muerto == true and sm1 == true and sm2==true and sm3==true) or (esta_muerto == false and (sm1 == false or sm2 == false or sm3 == false))),
                bpc integer NOT NULL CONSTRAINT bpc_less_than_zero CHECK(bpc >=0),
                cons integer NOT NULL,
                fu integer NOT NULL,
                des integer NOT NULL,
                sab integer NOT NULL,
                car integer NOT NULL,
                int integer NOT NULL,
                coordenadas_actuales text NOT NULL,
                vida_temp integer NOT NULL CONSTRAINT vida_temp_less_than_zero CHECK(vida_temp >=0),
                ca integer NOT NULL CHECK(ca >=0),
                edad integer NOT NULL CHECK(edad>0),
                peso integer NOT NULL CHECK(peso>0),
                pc integer NOT NULL CHECK(pc >=0),
                pp integer NOT NULL CHECK(pp >=0),
                pe integer NOT NULL CHECK(pe >=0),
                po integer NOT NULL CHECK(po >=0),
                ppt integer NOT NULL CHECK(ppt >=0),
                velocidad integer NOT NULL CONSTRAINT negative_velocidad_or_not_mult5 CHECK(((velocidad%5) == 0) and velocidad >0),
                descripcion_fisica text NOT NULL,
                tipo_raza text NOT NULL REFERENCES enum_raza(tipo_raza) ON UPDATE CASCADE ON DELETE CASCADE,
                tipo_clase text NOT NULL REFERENCES enum_clase(tipo_clase) ON UPDATE CASCADE ON DELETE CASCADE,
                tipo_alineamiento text NOT NULL REFERENCES enum_alineamiento(tipo_alineamiento) ON UPDATE CASCADE ON DELETE CASCADE,
                id_trasfondo integer NOT NULL REFERENCES trasfondo(num_trasfondo) ON UPDATE CASCADE ON DELETE CASCADE, 
                tipo_size text NOT NULL REFERENCES size(tipo_size) ON UPDATE CASCADE ON DELETE CASCADE,
                partida_id text NOT NULL REFERENCES partida(numPartida) ON DELETE CASCADE,
                id_jugador text REFERENCES jugador(id_jugador) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_id_jugador CHECK(num_npc_partida is NULL),
                num_npc_partida integer REFERENCES npc(num_npc_partida) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_num_npc_partida CHECK(id_jugador is NULL),
                PRIMARY KEY(partida_id,id_jugador,num_npc_partida,name) CONSTRAINT personaje_must_be_npc_or_jugador_in_pk CHECK((id_jugador is NULL and num_npc_partida is not NULL) or (id_jugador is not NULL and num_npc_partida is NULL))
            )
        """)
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador_personaje
                BEFORE UPDATE ON jugador
                BEGIN
                    UPDATE personaje
                    SET id_jugador = NEW.id_jugador
                    WHERE id_jugador = OLD.id_jugador;
                END;
        """
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_language (
                tipo_language text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comp_idioma (
                tipo_language text NOT NULL REFERENCES enum_language(tipo_language) ON UPDATE CASCADE ON DELETE CASCADE,
                name text NOT NULL REFERENCES personaje(name) ON UPDATE CASCADE ON DELETE CASCADE,
                partida_id text NOT NULL REFERENCES partida(numPartida) ON DELETE CASCADE,
                id_jugador text REFERENCES jugador(id_jugador) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_id_jugador_comp CHECK(num_npc_partida is NULL),
                num_npc_partida integer REFERENCES npc(num_npc_partida) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_num_npc_partida_comp CHECK(id_jugador is NULL),
                PRIMARY KEY(tipo_language,partida_id,id_jugador,num_npc_partida,name) CONSTRAINT personaje_must_be_npc_or_jugador_in_pk_comp CHECK((id_jugador is NULL and num_npc_partida is not NULL) or (id_jugador is not NULL and num_npc_partida is NULL))
            )
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador_comp_idioma
                BEFORE UPDATE ON jugador
                BEGIN
                    UPDATE comp_idioma
                    SET id_jugador = NEW.id_jugador
                    WHERE id_jugador = OLD.id_jugador;
                END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_caracteristicas (
                tipo_caracteristica text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_habilidades (
                tipo_habilidad text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salvaciones_comp (
                tipo_caracteristica text NOT NULL REFERENCES enum_caracteristicas(tipo_caracteristica) ON UPDATE CASCADE ON DELETE CASCADE,
                name text NOT NULL REFERENCES personaje(name) ON UPDATE CASCADE ON DELETE CASCADE,
                partida_id text NOT NULL REFERENCES partida(numPartida) ON DELETE CASCADE,
                id_jugador text REFERENCES jugador(id_jugador) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_id_jugador_comp CHECK(num_npc_partida is NULL),
                num_npc_partida integer REFERENCES npc(num_npc_partida) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_num_npc_partida_comp CHECK(id_jugador is NULL),
                PRIMARY KEY(tipo_caracteristica,partida_id,id_jugador,num_npc_partida,name) CONSTRAINT personaje_must_be_npc_or_jugador_in_pk_comp CHECK((id_jugador is NULL and num_npc_partida is not NULL) or (id_jugador is not NULL and num_npc_partida is NULL))
            )
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador_salvaciones_comp
                BEFORE UPDATE ON jugador
                BEGIN
                    UPDATE salvaciones_comp
                    SET id_jugador = NEW.id_jugador
                    WHERE id_jugador = OLD.id_jugador;
                END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habilidades_comp (
                tipo_habilidad text NOT NULL REFERENCES enum_habilidades(tipo_habilidad) ON UPDATE CASCADE ON DELETE CASCADE,
                name text NOT NULL REFERENCES personaje(name) ON UPDATE CASCADE ON DELETE CASCADE,
                partida_id text NOT NULL REFERENCES partida(numPartida) ON DELETE CASCADE,
                id_jugador text REFERENCES jugador(id_jugador) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_id_jugador_comp CHECK(num_npc_partida is NULL),
                num_npc_partida integer REFERENCES npc(num_npc_partida) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_num_npc_partida_comp CHECK(id_jugador is NULL),
                PRIMARY KEY(tipo_habilidad,partida_id,id_jugador,num_npc_partida,name) CONSTRAINT personaje_must_be_npc_or_jugador_in_pk_comp CHECK((id_jugador is NULL and num_npc_partida is not NULL) or (id_jugador is not NULL and num_npc_partida is NULL))
            )
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador_habilidades_comp
                BEFORE UPDATE ON jugador
                BEGIN
                    UPDATE habilidades_comp
                    SET id_jugador = NEW.id_jugador
                    WHERE id_jugador = OLD.id_jugador;
                END;
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enum_objeto_inventario (
                name text PRIMARY KEY
            )
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                cantidad integer NOT NULL CONSTRAINT cantidad_negativa CHECK(cantidad >=0),
                name_obj text NOT NULL REFERENCES enum_objeto_inventario(name) ON UPDATE CASCADE ON DELETE CASCADE,
                name text NOT NULL REFERENCES personaje(name) ON UPDATE CASCADE ON DELETE CASCADE,
                partida_id text NOT NULL REFERENCES partida(numPartida) ON DELETE CASCADE,
                id_jugador text REFERENCES jugador(id_jugador) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_id_jugador_comp CHECK(num_npc_partida is NULL),
                num_npc_partida integer REFERENCES npc(num_npc_partida) ON DELETE CASCADE CONSTRAINT personaje_must_be_npc_or_jugador_in_num_npc_partida_comp CHECK(id_jugador is NULL),
                PRIMARY KEY(name_obj,partida_id,id_jugador,num_npc_partida,name) CONSTRAINT personaje_must_be_npc_or_jugador_in_pk_comp CHECK((id_jugador is NULL and num_npc_partida is not NULL) or (id_jugador is not NULL and num_npc_partida is NULL))
            )
        """
        )
        cursor.execute(
            """
            CREATE TRIGGER IF NOT EXISTS actualizar_id_jugador_inventario
                BEFORE UPDATE ON jugador
                BEGIN
                    UPDATE inventario
                    SET id_jugador = NEW.id_jugador
                    WHERE id_jugador = OLD.id_jugador;
                END;
        """
        )
        conn.commit()
        #aseguramos la creación de las tablas
        data_enum_estado = [
            ["inactiva"],
            ["en progreso"],
            ["completada"]
        ]
        data_vinculos = [
            #Acólito
            (1, "Daría mi vida para recuperar una antigua reliquia de mi fe que se perdió hace mucho tiempo."),
            (2, "Algún día me vengaré de la corrupta jerarquía del templo que me tachó de hereje."),
            (3, "Le debo mi vida al sacerdote que me acogió cuando mis padres murieron."),
            (4, "Todo lo que hago es para la gente común."),
            (5, "Haré cualquier cosa para proteger el templo donde serví."),
            (6, "Busco preservar un texto sagrado que mis enemigos consideran herético y tratan de destruir."),
            #Artesano Gremial
            (7, "El taller donde aprendí mi oficio es el lugar más importante en el mundo para mí."),
            (8, "Creé una gran obra para alguien, y después lo encontré indigno de recibirla. Todavía busco a alguien que sea digno."),
            (9, "Le debo mucho a mi gremio por convertirme en la persona que ahora soy."),
            (10, "Busco riquezas para asegurarme el amor de alguien."),
            (11, "Algún día, volveré a mi gremio y probaré que soy el más grande artesano."),
            (12, "Me vengaré de las malvadas fuerzas que destruyeron mi lugar de trabajo y arruinaron mi estilo de vida."),
            #Artista
            (13, "Mi instrumento es mi posesión más preciada y me recuerda a alguien que amo."),
            (14, "Alguien robó mi preciado instrumento, y algún día lo recuperaré."),
            (15, "Quiero ser famoso, cueste lo que cueste."),
            (16, "Idolatro a un héroe de los viejos cuentos y mido mis actos conforme a los suyos."),
            (17, "Haré cualquier cosa para demostrarle mi superioridad a mi odiado rival."),
            (18, "Haría cualquier cosa por los demás miembros de mi antiguo grupo de teatro."),
            #Charlatán
            (19, "He esquilmado a la persona equivocada y debo asegurarme que este individuo nunca se cruce conmigo o con las personas que me importan."),
            (20, "Le debo todo a mi mentor, una persona horrible que probable-mente esté pudriéndose en alguna cárcel."),
            (21, "En algún lugar por ahí, tengo un hijo que no me conoce. Estoy haciendo un mundo mejor para él o ella."),
            (22, "Provengo de una familia noble, y un día reclamaré mis tierras y el título que me robaron."),
            (23, "Una persona poderosa mató a alguien a quien amaba. Alguno de estos días tendré mi venganza."),
            (24, "Estafé y arruiné a una persona que no lo merecía. He tratado de expiar mis malas acciones, pero nunca pude perdonármelo."),
            #Criminal
            (25, "Estoy tratando de saldar una vieja deuda que le debo a un generoso benefactor."),
            (26, "Mis mal obtenidas ganancias son para mantener a mi familia."),
            (27, "Algo importante me fue substraído y mi objetivo es robarlo de nuevo."),
            (28, "Seré el ladrón más grande que jamás haya existido."),
            (29, "Soy culpable de un terrible crimen. Espero que pueda redimirme por ello."),
            (30, "Alguien que amaba murió a causa de un error que cometí. Nunca volverá a suceder."),
            #Ermitaño
            (31, "Nada es más importante que los demás miembros de mi orden o asociación ermitaña."),
            (32, "Me recluí para ocultarme de aquellos que aun me deben estar dando caza. Algún día deberé confrontarlos."),
            (33, "Aun busco la iluminación que perseguía durante mi reclusión, y aun me elude."),
            (34, "Entré en reclusión por que amaba a alguien a quien no podía tener."),
            (35, "Si aquello que descubrí saliera a la luz, traería la ruina al mundo."),
            (36, "Mi aislamiento me ha dado una gran comprensión sobre un gran mal que solo yo puedo destruir."),
            #Forastero
            (37, "Mi familia, clan o tribu es lo más importante en mi vida, incluso cuando están lejos de mí."),
            (38, "Una agresión contra las tierras vírgenes de mi hogar es una agresión contra mi persona."),
            (39, "Arrojaré mi terrible ira sobre los criminales que destruyeron mi patria."),
            (40, "Soy el último de mi tribu y a mí me corresponde asegurar que sus nombres se conviertan en leyenda."),
            (41, "Sufro unas espantosas visiones de un desastre que se avecina y haré cualquier cosa para evitarlo."),
            (42, "Es mi deber de proporcionar descendencia a mi tribu para su perpetuación."),
            #Héroe del pueblo
            (43, "Tengo una familia, pero no tengo ni idea de dónde están. Un día, espero volver a verlos."),
            (44, "He trabajado la tierra, yo amo la tierra, y la protegeré."),
            (45, "Un orgulloso noble una vez me dio una terrible paliza, y voy a vengarme de cualquier bravucón que me encuentre."),
            (46, "Mis herramientas son símbolos de mi vida pasada, y los llevo por lo que nunca voy a olvidar mis raíces."),
            (47, "Protejo a quienes no pueden protegerse a sí mismos."),
            (48, "Me gustaría que mi novia de la infancia hubiera venido conmigo a perseguir mi destino."),
            #Huérfano
            (49, "Mi pueblo o ciudad es mi hogar, y lucharé para defenderlo."),
            (50, "Mantengo un orfanato para evitar que otros soporten lo que yo tuve que soportar."),
            (51, "Le debo mi vida a otro huérfano que me enseñó a vivir en las calles."),
            (52, "Tengo una deuda que nunca podré pagar con alguien que me tuvo lástima."),
            (53, "Escapé de mi vida de pobreza robándole a alguien importante, y me buscan por eso."),
            (54, "Nadie tendría que soportar una vida tan dura como la mía."),
            #Marinero
            (55, "Soy leal primero a mi capitán. Todo lo demás está en segundo plano."),
            (56, "El barco es lo más importante —las tripulaciones y los capitanes van y vienen."),
            (57, "Siempre recordaré mi primer barco."),
            (58, "En un puerto tengo un amante cuyos ojos casi le roban mi corazón al mar."),
            (59, "Me estafaron mi justa parte de las ganancias, y quiero cobrar mi deuda."),
            (60, "Despiadados piratas asesinaron a mi tripulación y mi capitán, hundieron mi barco y me abandonaron a mi suerte. La venganza será mía."),
            #Noble
            (61, "Afrontaré cualquier reto con tal de conseguir la aprobación de mi familia."),
            (62, "La alianza de mi Casa con otra familia noble debe ser mantenida a cualquier precio."),
            (63, "Nadie es más importante que los otros miembros de mi familia."),
            (64, "Estoy enamorado/a de un heredero (o heredera) de una familia que es despreciada por la mía."),
            (65, "Mi lealtad a la corona es inquebrantable."),
            (66, "La gente común debe verme como un héroe de la gente."),
            #Sabio
            (67, "Es mi deber de proteger a mis alumnos."),
            (68, "Tengo un texto antiguo que guarda terribles secretos que no deben caer en manos equivocadas."),
            (69, "Trabajo para preservar una biblioteca, universidad, scriptorium, o monasterio."),
            (70, "El trabajo de mi vida es una serie de tomos relacionados con un campo específico del conocimiento."),
            (71, "He estado buscando toda mi vida la respuesta a una pregunta determinada."),
            (72, "He vendido mi alma por el conocimiento. Espero hacer grandes hazañas y ganarla de nuevo."),
            #Soldado
            (73, "Aún daría mi vida por las personas con las que serví."),
            (74, "Alguien me salvó la vida en el campo de batalla. Hasta la fecha, nunca dejaré atrás a un amigo."),
            (75, "Mi honor es mi vida."),
            (76, "Nunca olvidaré la derrota aplastante que sufrió mi compañía o a los enemigos que la causaron."),
            (77, "Los que luchan junto a mí son por los que vale la pena morir."),
            (78, "Yo lucho por los que no pueden luchar por sí mismos.")
        ]
        data_defectos = [
            #Acólito
            (1, "Juzgo a otros con dureza, y a mí mismo aún más severamente."),
            (2, "Pongo demasiada confianza en quienes ejercen el poder dentro de la jerarquía de mi templo."),
            (3, "Mi piedad a veces me lleva a confiar ciegamente en los que profesan la fe en mi Dios."),
            (4, "Soy inflexible en mi pensamiento."),
            (5, "Soy desconfiado con los extraños y espero lo peor de ellos."),
            (6, "Una vez que tengo un objetivo, me obsesiono con él en detrimento de todo lo demás en mi vida."),
            #Artesano Gremial
            (7, "Haré cualquier cosa para poner mis manos sobre algo raro o valioso."),
            (8, "Rápidamente asumo que la gente trata de engañarme."),
            (9, "Nadie debe saber que una vez robé de las arcas del gremio."),
            (10, "Nunca estoy satisfecho con lo que tengo —siempre quiero más."),
            (11, "Mataría para adquirir un título de nobleza."),
            (12, "Estoy horriblemente celoso de cualquiera que pueda eclipsar mi trabajo manual. Donde quiera que vaya, estoy rodeado por rivales."),
            #Artista
            (13, "Haré cualquier cosa para obtener fama y renombre."),
            (14, "Me pierdo por una cara bonita."),
            (15, "Un escándalo me impide volver a mi hogar. Este tipo de problemas parecen perseguirme."),
            (16, "Una vez ridiculicé a un noble que todavía quiere mi cabeza. Fue un error que probablemente vuelva a repetir."),
            (17, "Tengo problemas para mantener mis verdaderos sentimientos ocultos. Mi afilada lengua me suele meter en líos."),
            (18, "A pesar de mis esfuerzos, para mis amigos no soy una persona de fiar."),
            #Charlatán
            (19, "No puedo resistirme a una cara bonita."),
            (20, "Siempre estoy endeudado. Gasto mis mal adquiridas ganancias en lujos decadentes más rápido de lo que las obtengo."),
            (21, "Estoy convencido de que nadie me puede engañar del modo en que yo engaño a los demás."),
            (22, "Soy demasiado codicioso para mi propia seguridad. No puedo resistir a arriesgarme si hay dinero involucrado."),
            (23, "No puedo resistirme a estafar a la gente que es más poderosa que yo."),
            (24, "Odio admitirlo y me odiaré a mí mismo por ello, pero voy a correr y conservar mi propio pellejo si las cosas se ponen difíciles."),
            #Criminal
            (25, "Cuando veo algo valioso, no puedo pensar en nada más que en la forma de robarlo."),
            (26, "Cuando me enfrento a una elección entre el dinero y mis amigos, por lo general elijo el dinero."),
            (27, "Si hay un plan, lo olvidaré. Si no lo olvido, lo ignoraré."),
            (28, "Tengo un “algo” que revela cuándo estoy mintiendo."),
            (29, "Cuando las cosas se ponen feas, doy la vuelta y corro."),
            (30, "Una persona inocente está en la cárcel por un crimen que cometí. Y no me arrepiento de ello."),
            #Ermitaño
            (31, "Ahora que he regresado al mundo, disfruto sus deleites quizás demasiado."),
            (32, "Tengo pensamientos obscuros y sanguinarios que mi aislamiento y meditación no pudieron remediar."),
            (33, "Soy dogmático en cuanto a mis pensamientos y filosofía."),
            (34, "Permito que mi necesidad por ganar discusiones se anteponga a la amistad y la armonía."),
            (35, "Podría arriesgar mucho para descubrir un poco de conocimiento perdido."),
            (36, "Me gusta guardar secretos y no los compartiría con nadie."),
            #Forastero
            (37, "Soy demasiado aficionado a la cerveza, el vino y otras bebidas embriagantes."),
            (38, "No hay lugar para la precaución cuando se vive al máximo."),
            (39, "Recuerdo todos los insultos que he recibido y albergo un resentimiento silencioso hacia toda persona que alguna vez me ha ofendido."),
            (40, "Tardo mucho en confiar en los miembros de otras razas, tribus y sociedades."),
            (41, "La violencia es mi respuesta a casi cualquier desafío."),
            (42, "No esperes que salve a los que no pueden salvarse sí mismos. Es la manera en la que la naturaleza hace que el fuerte prospere y que el débil perezca."),
            #Héroe del pueblo
            (43, "El tirano que gobierna mi tierra no se detendrá ante nada con tal de verme muerto."),
            (44, "Estoy convencido de la importancia de mi destino, y ciego frente a mis carencias y el riesgo de fracasar."),
            (45, "Las personas que me conocieron cuando era joven conocen mi vergonzoso secreto, así que nunca puedo volver a casa de nuevo."),
            (46, "Tengo una debilidad por los vicios de la ciudad, especialmente por la bebida en grandes cantidades."),
            (47, "En secreto, creo que las cosas estarían mejor si yo fuera un tirano con su señorío."),
            (48, "Tengo problemas para confiar en mis aliados."),
            #Huérfano
            (49, "Si me veo superado en número, correré por mi vida."),
            (50, "Un oro me parece un montón de dinero, y haré casi cualquier cosa por más de eso."),
            (51, "Nunca confiaré totalmente en nadie más que en mí mismo."),
            (52, "Preferiría matar a alguien mientras duerme a enfrentarme en un combate justo."),
            (53, "Si yo necesito algo más que lo que lo necesita su dueño, no es un robo."),
            (54, "La gente que no puede cuidarse de sí misma obtiene lo que merece."),
            #Marinero
            (55, "Seguiré las órdenes, incluso si creo que son equivocadas."),
            (56, "Diré cualquier cosa para evitar tener que trabajar de más."),
            (57, "Una vez que alguien cuestiona mi coraje, nunca me retracto, sin importar lo peligrosa de la situación."),
            (58, "Una vez que comienzo a beber, es muy difícil que pare."),
            (59, "No puedo evitar guardarme monedas sueltas y otras baratijas que encuentro."),
            (60, "Mi orgullo probablemente me llevará a la destrucción."),
            #Noble
            (61, "Secretamente pienso que todo el mundo está por debajo de mi."),
            (62, "Escondo un secreto verdaderamente escandaloso que podría arruinar a mi familia para siempre."),
            (63, "Muy a menudo escucho velados insultos y amenazas en cada palabra que me dirigen y me enfado con rapidez."),
            (64, "Tengo un insaciable apetito por los placeres carnales."),
            (65, "Es un hecho que el mundo gira a mi alrededor"),
            (66, "Debido a mis palabras y acciones, suelo traer la vergüenza a mi familia."),
            #Sabio
            (67, "Me distraigo con facilidad por promesas de información."),
            (68, "La mayoría de las personas gritan y corren cuando ven a un demonio. Yo me detengo y tomo notas sobre su anatomía."),
            (69, "Desenterrar un antiguo misterio bien vale el precio de una civilización."),
            (70, "Paso por alto soluciones obvias a favor de las complicadas."),
            (71, "Hablo sin detenerme a pensar mis palabras, invariablemente insultando a los demás."),
            (72, "No puedo guardar un secreto para salvar mi vida, o la de cualquier otro."),
            #Soldado
            (73, "El monstruoso enemigo que nos enfrentamos en batalla todavía me deja temblando de miedo."),
            (74, "Tengo poco respeto por cualquiera que no sea un guerrero probado en batalla."),
            (75, "Cometí un error terrible en batalla que costó muchas vidas y haría cualquier cosa para mantener ese error en secreto."),
            (76, "Mi odio hacia mis enemigos es ciego e irracional."),
            (77, "Yo obedezco la ley, aunque la ley genere miseria."),
            (78, "Preferiría comerme mi armadura antes que admitir mis errores.")
        ]
        data_ideales = [
            #Acólito
            (1, "Tradición. Las antiguas tradiciones de culto y sacrificio deben ser preservadas y defendidas."),
            (2, "Caridad. Yo siempre trato de ayudar a los necesitados, sin importar el coste personal."),
            (3, "Cambio. Debemos ayudar para que se logren los cambios que los dioses maquilan constantemente para el mundo."),
            (4, "Poder. Espero llegar algún día a la cima de la jerarquía religiosa de mi fe."),
            (5, "Fe. Confío en que mi deidad guiará mis acciones. Tengo fe en que si trabajo duro, las cosas irán bien."),
            (6, "Aspiración. Trato de probarme a mí mismo ser merecedor de los favores de mi dios, comparando mis acciones con sus enseñanzas."),
            #Artesano Gremial
            (7, "Comunidad. Es el deber de todas las personas civilizadas reforzar los vínculos de la comunidad y la seguridad de la civilización."),
            (8, "Generosidad. Mis talentos me fueron dados para que pudiera usarlos para beneficiar al mundo."),
            (9, "Libertad. Cada uno debería ser libre de perseguir su propio estilo de vida."),
            (10, "Avaricia. Sólo estoy en esto por el dinero."),
            (11, "Gente. Estoy comprometido con la gente que me importa, no con un ideal."),
            (12, "Aspiración. Trabajo duro para ser el mejor en mi oficio."),
            #Artista
            (13, "Belleza. Cuando actúo, hago del mundo algo mejor de lo que era."),
            (14, "Tradición. Las historias, leyendas y canciones del pasado nunca deberían ser olvidadas, porque nos enseñan quiénes somos."),
            (15, "Creatividad. El mundo está necesitado de ideas nuevas y acciones audaces."),
            (16, "Codicia. Sólo estoy en esto por el dinero y la fama."),
            (17, "Personas. Me gusta ver las sonrisas en las caras de las personas cuando actúo. Eso es todo lo que importa."),
            (18, "Honestidad. El arte debe reflejar el alma; debe salir de dentro y revelar lo que realmente somos."),
            #Charlatán
            (19, "Independencia. Soy un espíritu libre, nadie me dice lo que he de hacer."),
            (20, "Equidad. Nunca estafo a gente que no se pueda permitir el lujo de perder unas cuantas monedas."),
            (21, "Caridad. Distribuyo el dinero que adquiero a la gente que realmente lo necesita."),
            (22, "Creatividad. Nunca utilizo la misma estafa dos veces."),
            (23, "Amistad. Los bienes materiales van y vienen. Los vínculos de la amistad duran para siempre."),
            (24, "Aspiración. Estoy decidido a hacer algo de mí mismo."),
            #Criminal
            (25, "Honor. No robo a otros de mi grupo."),
            (26, "Libertad. Las cadenas están hechas para romperse, así como aquellos que las forjan."),
            (27, "Caridad. Robo a los ricos para poder ayudar a las personas necesitadas."),
            (28, "Codicia. Haré todo lo necesario para convertirme en alguien rico."),
            (29, "Personas. Soy leal a mis amigos, no a los ideales, y si por mi fuera, el resto del mundo puede ir a hacerse un viaje por la laguna Estigia."),
            (30, "Redención. Hay una chispa de bondad en todos."),
            #Ermitaño
            (31, "Bien Mayor. Mis dones están destinados a ser compartidos con todos, no a ser usados para mi propio beneficio."),
            (32, "Lógica. Las emociones no deben nublar nuestro sentido de lo que es correcto y verdadero, o nuestro razonamiento lógico."),
            (33, "Libre Pensamiento. La investigación y la curiosidad son los pilares del progreso."),
            (34, "Poder. La soledad y la contemplación son caminos para el poder místico o mágico."),
            (35, "Vive y Deja Vivir. Inmiscuirse en los asuntos de otros sólo genera problemas."),
            (36, "Auto-Conocimiento. Si te conoces a ti mismo, no hay nada más que conocer."),
            #Forastero
            (37, "Cambio. La vida es como las estaciones del año, en constante cambio, y debemos cambiar con ella."),
            (38, "Bien Mayor. Es responsabilidad de cada persona procurar la má-xima felicidad para la totalidad de la tribu."),
            (39, "Honor. Si me deshonro a mí mismo, deshonro a todo mi clan."),
            (40, "Poder. Los más fuertes están destinados a gobernar."),
            (41, "Naturaleza. El mundo natural es más importante que todas las creaciones de la civilización."),
            (42, "Gloria. Debo ganar gloria en batalla, para mí y para mi clan."),
            #Héroe del pueblo
            (43, "Respeto. Las personas merecen ser tratadas con dignidad y respeto."),
            (44, "Equidad. Nadie debe tener un trato preferencial ante la ley y nadie está por encima de la ley."),
            (45, "Libertad. A los tiranos no se les debe permitir oprimir al pueblo."),
            (46, "Poder. Si me hago fuerte, podré tomar lo que quiero, lo que yo merezco."),
            (47, "Sinceridad. No hay nada bueno en pretender ser algo que no soy."),
            (48, "Destino. Nada ni nadie me puede desviar de mi más alta vocación."),
            #Huérfano
            (49, "Respeto. Todo el mundo, sin importar su riqueza, merece respeto."),
            (50, "Comunidad. Tenemos que cuidarnos el uno al otro, porque nadie más lo hará."),
            (51, "Cambio. Los que están abajo ascienden y los poderosos que están arriba son derribados. El cambio es la naturaleza de las cosas."),
            (52, "Retribución. Los ricos necesitan que les muestren cómo son la vida y la muerte en las cloacas."),
            (53, "Gente. Ayudo a quienes me ayudan –eso es lo que nos mantiene vivos."),
            (54, "Aspiración. Voy a probar que merezco una vida mejor."),
            #Marinero
            (55, "Respeto. Lo que mantiene una nave funcionando es el respeto mutuo entre capitán y tripulación."),
            (56, "Equidad. Todos trabajamos, así que todos compartimos la recompensa."),
            (57, "Libertad. El mar es libertad —la libertad de ir a cualquier lado y hacer cualquier cosa."),
            (58, "Autoridad. Soy un predador, y los demás barcos en el mar, mi presa."),
            (59, "Gente. Estoy comprometido con mi tripulación, no con un ideal."),
            (60, "Aspiración. Algún día, tendré mi propio barco y forjaré mi propio destino."),
            #Noble
            (61, "Respeto. Se me debe respeto debido a mi posición, pero toda la gente sin importar su posición social, debe ser tratada con dignidad."),
            (62, "Responsabilidad. Es mi deber respetar a la autoridad de aquellos por encima de mí, así como los que están por debajo de mí deben respetarme."),
            (63, "Independencia. Debo probar que puedo encargarme de mí mismo, sin la protección de mi familia"),
            (64, "Poder. Si obtengo más poder, nadie podrá decirme qué hacer."),
            (65, "Familia. La sangre fluye más espesa que el agua."),
            (66, "Obligación noble. Es mi deber proteger y cuidar a aquellos por debajo de mí."),
            #Sabio
            (67, "Conocimiento. El camino hacia el poder y la autosuperación es a través del conocimiento."),
            (68, "Belleza. Lo que es bello nos lleva más allá de sí mismo hacia lo que es verdadero."),
            (69, "Lógica. Las emociones no deben nublar nuestro pensamiento lógico."),
            (70, "Sin límites. Nada debe estorbar la posibilidad infinita inherente a toda existencia."),
            (71, "Poder. El conocimiento es el camino hacia el poder y la dominación."),
            (72, "Autosuperación. La meta de una vida de estudio es la mejora de uno mismo."),
            #Soldado
            (73, "Bien mayor. Nuestro destino es dar nuestra vida en defensa de los demás."),
            (74, "Responsabilidad. Hago lo que debo y obedezco a la autoridad justa."),
            (75, "Independencia. Cuando las personas siguen las órdenes ciegamente, abrazan una especie de tiranía."),
            (76, "Poder. En la vida como en la guerra, los más fuertes ganan."),
            (77, "Vive y deja vivir. No vale la pena matar o ir a la guerra por los ideales."),
            (78, "Nación. Mi ciudad, mi nación o mi gente son todo lo que importa.")
        ]
        data_rasgos_personalidad = [
            #Acólito
            (1, "Idolatro a un héroe en particular de mi fe, y hago referencia constantemente a las vivencias y el ejemplo de esa persona."),
            (2, "Puedo encontrar un objetivo común hasta con los enemigos más feroces, empatizar con ellos y trabajar siempre hacia la paz."),
            (3, "Veo presagios en cualquier acontecimiento y acción. Los dioses tratan de hablar con nosotros, sólo tenemos que escuchar"),
            (4, "Nada puede hacer tambalear mi actitud optimista."),
            (5, "Cito (o incorrectamente cito) los textos sagrados y proverbios en casi cualquier situación."),
            (6, "Soy tolerante (o intolerante) hacia otras religiones y respeto (o condeno) la adoración de otros dioses."),
            (7, "He disfrutado de la buena comida, bebida y la alta sociedad entre la élite de mi templo. Me incomoda la vida ruda."),
            (8, "He pasado tanto tiempo en el templo que tengo poca experiencia práctica en el trato con personas del mundo exterior."),
            #Artesano Gremial
            (9, "Creo que cualquier cosa que valga la pena hacerse, vale la pena hacerlo bien. No puedo evitarlo —Soy un perfeccionista."),
            (10, "Soy un engreído que mira con desprecio a aquellos que no pueden apreciar el arte."),
            (11, "Siempre quiero saber cómo funcionan las cosas y qué mueve a la gente."),
            (12, "Conozco cientos de ingeniosos aforismos y tengo un proverbio para cada ocasión."),
            (13, "Soy grosero con la gente que no tiene mi compromiso por el trabajo duro y las reglas justas."),
            (14, "Me gusta hablar largo y tendido sobre mi profesión."),
            (15, "No me separo con facilidad de mi dinero y regatearé para conseguir el mejor trato posible."),
            (16, "Soy bien conocido por mi trabajo, y quiero asegurarme de que todo el mundo lo aprecia. Siempre me sorprende cuando alguien no ha oído hablar de mí."),
            #Artista
            (17, "Conozco una historia relevante para casi todas las situaciones."),
            (18, "Cada vez que vengo a un lugar nuevo, colecciono rumores locales y difundo chismes."),
            (19, "Soy un romántico empedernido, siempre en busca de “ese alguien especial”."),
            (20, "Nadie permanece enfadado conmigo o a mi alrededor durante mucho tiempo, ya que puedo disipar cualquier cantidad de tensión."),
            (21, "Me encanta un buen insulto, incluso uno dirigido a mí."),
            (22, "Mi carácter se amarga si no soy el centro de atención."),
            (23, "Sólo me conformo con la perfección."),
            (24, "Puedo cambiar mi estado de ánimo o mi manera de pensar tan rápido como le cambio la tonalidad en una canción."),
            #Charlatán
            (25, "Me enamoro con facilidad y siempre estoy persiguiendo alguien."),
            (26, "Tengo una broma para cada ocasión, en especial en ocasiones en las que el humor es inapropiado."),
            (27, "La adulación es mi truco preferido para conseguir lo que quiero."),
            (28, "Soy un jugador nato que no puede resistirse a arriesgarse por una potencial recompensa."),
            (29, "Miento sobre casi todo, incluso cuando no hay una buena razón para hacerlo."),
            (30, "El sarcasmo y los insultos son mis armas predilectas."),
            (31, "Llevo encima varios símbolos sagrados e invoco a cualquier deidad que pueda resultarme útil en el momento."),
            (32, "Me meto en el bolsillo cualquier cosa que parezca que pueda tener algún valor."),
            #Criminal
            (33, "Siempre tengo un plan sobre qué hacer cuando las cosas van mal."),
            (34, "Siempre estoy tranquilo, no importa cuál sea la situación. Nunca levanto la voz o dejo que mis emociones me controlen."),
            (35, "La primera cosa que hago en un lugar nuevo es tomar nota de las ubicaciones de todo lo valioso, o dónde podrían estar ocultas dichas cosas."),
            (36, "Prefiero hacer un nuevo amigo que un nuevo enemigo."),
            (37, "Soy increíblemente lento en fiarme de alguien. Aquellos que parecen los más justos a menudo tienen más que ocultar."),
            (38, "No presto atención a los riesgos de una situación. Nunca me digan las posibilidades de tener o no éxito."),
            (39, "La mejor manera de que llegue a hacer algo es decirme que no puedo hacerlo."),
            (40, "Golpeo al menor insulto."),
            #Ermitaño
            (41, "Estuve aislado por tanto tiempo que raramente hablo, prefiriendo los gestos y algún gruñido ocasional."),
            (42, "Estoy absolutamente calmado, incluso ante el desastre."),
            (43, "El líder de mi comunidad tenía algo sabio que decir sobre todos los temas, y estoy deseoso de compartir su sabiduría."),
            (44, "Siento tremenda empatía por todos los que sufren."),
            (45, "No soy consciente de la etiqueta y las expectativas sociales."),
            (46, "Conecto todo lo que me ocurre con un gran plan cósmico."),
            (47, "A menudo me pierdo en mis propios pensamientos, sin ser consciente de mi entorno."),
            (48, "Trabajo en una gran teoría filosófica y amo compartir mis ideas."),
            #Forastero
            (49, "Me impulsa una pasión por los viajes que me condujo muy lejos de mi hogar."),
            (50, "Cuido a mis amigos como si fueran una camada de cachorros recién nacidos."),
            (51, "Una vez corrí veinticinco millas sin parar para advertir a mi clan que una horda de orcos se aproximaba. Lo haría de nuevo si tuviera que hacerlo."),
            (52, "Tengo una lección para cada situación, extraída a partir de la observación de la naturaleza."),
            (53, "No tengo muy buena opinión de la gente adinerada o de buenos modales. El dinero y los modales no te salvarán de un oso-lechuza hambriento."),
            (54, "Siempre estoy cogiendo cosas, toqueteándolas con aire ausente y, a veces, rompiéndolas."),
            (55, "Me siento mucho más cómodo con los animales que con las personas."),
            (56, "Fui, de hecho, criado por los lobos."),
            #Héroe del pueblo
            (57, "Juzgo a la gente por sus acciones, no sus palabras."),
            (58, "Si alguien está en problemas, siempre estoy dispuesto a prestar ayuda."),
            (59, "Cuando me propongo algo, lo persigo sin importarme lo que se interponga en mi camino."),
            (60, "Tengo un fuerte sentido del juego limpio y siempre trato de encontrar la solución más equitativa a las discusiones."),
            (61, "Tengo confianza en mis propias capacidades y haré lo que pueda para inspirar confianza en los demás."),
            (62, "Pensar es para otros. Yo prefiero la acción."),
            (63, "Hago mal uso de palabras largas en un intento de parecer más inteligente."),
            (64, "Me aburro fácilmente. ¿Cuándo voy a seguir adelante con mi destino?"),
            #Huérfano
            (65, "Escondo trozos de comida y baratijas en mis bolsillos."),
            (66, "Hago un montón de preguntas."),
            (67, "Me gusta escabullirme en pequeños huecos donde nadie puede alcanzarme."),
            (68, "Duermo con mi espalda contra un árbol o un muro, con todas mis cosas envueltas en un paquete entre mis brazos."),
            (69, "Como como un cerdo y tengo malos modales."),
            (70, "Pienso que todos los que son amables conmigo esconden un propósito maligno."),
            (71, "No me gusta bañarme."),
            (72, "Digo francamente lo que otros insinúan o esconden."),
            #Marinero
            (73, "Mis amigos saben que pueden confiar en mí, sin importar la ocasión."),
            (74, "Trabajo duro para poder divertirme cuando el trabajo esté hecho."),
            (75, "Disfruto viajar a nuevos puertos y hacer nuevos amigos junto a jarras de cerveza."),
            (76, "Deformo la verdad por el bien de una buena historia."),
            (77, "Para mí, una pelea de taberna es una buena manera de conocer una nueva ciudad."),
            (78, "Nunca dejo pasar a un apostador amistoso."),
            (79, "Mi habla es tan desagradable como el cuello de un otyugh."),
            (80, "Me gusta el trabajo bien hecho. Sobre todo si puedo convencer a otro de que lo haga."),
            #Noble
            (81, "Mi elocuente adulación hace sentir a mi interlocutor la persona más importante y maravillosa del mundo."),
            (82, "La gente común me quiere por mi amabilidad y generosidad."),
            (83, "Nadie que mire mi regia postura puede dudar que esté por encima de las sucias masas."),
            (84, "Hago grandes esfuerzos para lucir siempre lo mejor posible y seguir las últimas modas."),
            (85, "No me gusta ensuciarme las manos, y no seré atrapado jamás en alojamientos inadecuados."),
            (86, "A pesar de mi noble cuna, no me coloco por encima del resto de la gente. Todos tenemos la misma sangre."),
            (87, "Mi favor, una vez perdido, es para siempre."),
            (88, "Si me haces daño, te aplastaré, arruinaré tu nombre y salaré a tus campos."),
            #Sabio
            (89, "Uso polisílabos para dar la impresión de gran erudición."),
            (90, "He leído todos los libros de las mayores bibliotecas del mundo, o me gusta presumir que lo he hecho."),
            (91, "Estoy acostumbrado a ayudar a aquellos que no son tan inteligentes como yo, y explico pacientemente una y otra vez cualquier cosa."),
            (92, "No hay nada que me guste más que un buen misterio."),
            (93, "Estoy dispuesto a escuchar todas las partes de una discusión antes de formarme un juicio propio."),
            (94, "Yo... hablo… lentamente... cuando hablo... para idiotas,... que... casi... todos... lo son... comparándose... conmigo."),
            (95, "Me siento horriblemente, horriblemente incómodo en situaciones sociales."),
            (96, "Estoy convencido de que la gente siempre está tratando de robar mis secretos."),
            #Soldado
            (97, "Siempre soy educado y respetuoso."),
            (98, "Los recuerdos de la guerra me persiguen. No puedo sacar las imágenes violentas de mi cabeza."),
            (99, "He perdido muchos amigos, y tardo mucho en hacer nuevos."),
            (100, "Estoy lleno de cuentos inspiradores y con moraleja de mi experiencia militar relevantes para casi todas las situación es de combate."),
            (101, "Puedo sostener la mirada a un perro infernal sin pestañear."),
            (102, "Disfruto siendo fuerte y me gusta romper cosas."),
            (103, "Tengo un vulgar sentido del humor."),
            (104, "Me enfrento a los problemas de frente. Una solución simple y directa es el mejor camino hacia el éxito.")
        ]
        data_enum_trasfondo = [
            ["Acólito"],
            ["Artesano Gremial"],
            ["Artista"],
            ["Charlatán"],
            ["Criminal"],
            ["Ermitaño"],
            ["Forastero"],
            ["Héroe del pueblo"],
            ["Huérfano"],
            ["Marinero"],
            ["Noble"],
            ["Sabio"],
            ["Soldado"]
        ]
        data_enum_raza = [
            ["Enano"],
            ["Elfo"],
            ["Mediano"],
            ["Humano"],
            ["Dracónido"],
            ["Gnomo"],
            ["Semielfo"],
            ["Semiorco"],
            ["Tiflin"]
        ]
        data_enum_clase = [
            ["Bárbaro"],
            ["Bardo"],
            ["Brujo"],
            ["Clérigo"],
            ["Druida"],
            ["Explorador"],
            ["Guerrero"],
            ["Hechicero"],
            ["Mago"],
            ["Monje"],
            ["Paladín"],
            ["Pícaro"]
        ]
        data_enum_alineamiento = [
            ["Legal Bueno"],
            ["Neutral Bueno"],
            ["Caótico Bueno"],
            ["Legal Neutral"],
            ["Neutral"],
            ["Caótico Neutral"],
            ["Legal Malvado"],
            ["Neutral Malvado"],
            ["Caótico Malvado"]
        ]
        data_size = [
            ["Diminuto"],
            ["Minúsculo"],
            ["Pequeño"],
            ["Mediano"],
            ["Grande"],
            ["Enorme"],
            ["Gigantesco"],
            ["Colosal"]
        ]
        data_enum_language = [
            ["Común"],
            ["Enano"],
            ["Élfico"],
            ["Infernal"],
            ["Celestial"],
            ["Abisal"],
            ["Dracónido"],
            ["Habla Profunda"],
            ["Primordial"],
            ["Silvano"],
            ["Infracomún"]
        ]
        data_enum_caracteristicas = [
            ["Constitución"],
            ["Fuerza"],
            ["Destreza"],
            ["Sabiduría"],
            ["Carisma"],
            ["Inteligencia"]
        ]
        data_enum_habilidades = [
            ["Acrobacias"],
            ["Atletismo"],
            ["Conocimiento Arcano"],
            ["Engaño"],
            ["Historia"],
            ["Interpretación"],
            ["Intimidación"],
            ["Investigación"],
            ["Juego de Manos"],
            ["Medicina"],
            ["Naturaleza"],
            ["Percepción"],
            ["Perspicacia"],
            ["Persuasión"],
            ["Religión"],
            ["Sigilo"],
            ["Supervivencia"],
            ["Trato con Animales"]
        ]
        
        query_enum_estado = """INSERT INTO enum_estado
                          (estado_quest) 
                          VALUES (?)"""
        query_vinculos = """INSERT INTO vinculos
                          (num_id, vinculo) 
                          VALUES (?,?)"""
        query_defectos = """INSERT INTO defectos
                          (num_id, defecto) 
                          VALUES (?,?)"""
        query_ideales = """INSERT INTO ideales
                          (num_id, ideal) 
                          VALUES (?,?)"""
        query_rasgos = """INSERT INTO rasgos_personalidad
                          (num_id, rasgo_personalidad) 
                          VALUES (?,?)"""
        query_trasfondo = """INSERT INTO enum_trasfondo
                          (tipo_trasfondo) 
                          VALUES (?)"""
        query_raza = """INSERT INTO enum_raza
                          (tipo_raza) 
                          VALUES (?)"""
        query_clase = """INSERT INTO enum_clase
                          (tipo_clase) 
                          VALUES (?)"""
        query_alineamiento = """INSERT INTO enum_alineamiento
                          (tipo_alineamiento) 
                          VALUES (?)"""
        query_size = """INSERT INTO size
                          (tipo_size) 
                          VALUES (?)"""
        query_enum_langauge = """INSERT INTO enum_language
                          (tipo_language) 
                          VALUES (?)"""
        query_enum_caracteristicas = """INSERT INTO enum_caracteristicas
                          (tipo_caracteristica) 
                          VALUES (?)"""
        query_enum_habilidades = """INSERT INTO enum_habilidades
                          (tipo_habilidad) 
                          VALUES (?)"""
        try:
            cursor.executemany(query_enum_estado, data_enum_estado)
        except:
            #no hacemos nada, los datos ya estaban en la tabla
            pass
        try:
            cursor.executemany(query_vinculos, data_vinculos)
        except:
            pass
        try:
            cursor.executemany(query_defectos, data_defectos)
        except:
            pass
        try:
            cursor.executemany(query_ideales, data_ideales)
        except:
            pass
        try:
            cursor.executemany(query_rasgos, data_rasgos_personalidad)
        except:
            pass
        try:
            cursor.executemany(query_trasfondo,data_enum_trasfondo)
        except:
            pass
        try:
            cursor.executemany(query_raza,data_enum_raza)
        except:
            pass
        try:
            cursor.executemany(query_clase,data_enum_clase)
        except:
            pass
        try:
            cursor.executemany(query_alineamiento,data_enum_alineamiento)
        except:
            pass
        try:
            cursor.executemany(query_size,data_size)
        except:
            pass
        try:
            cursor.executemany(query_enum_langauge,data_enum_language)
        except:
            pass
        try:
            cursor.executemany(query_enum_caracteristicas,data_enum_caracteristicas)
        except:
            pass
        try:
            cursor.executemany(query_enum_habilidades,data_enum_habilidades)
        except:
            pass
        conn.commit()
        conn.close()

        
        

        