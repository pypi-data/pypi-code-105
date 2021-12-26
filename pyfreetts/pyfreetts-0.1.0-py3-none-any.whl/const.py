INIT_DATABASE = """
DROP TABLE IF EXISTS "voice";
DROP TABLE IF EXISTS "language";

-- Create table statement
CREATE TABLE "language" (
    "id"    TEXT NOT NULL UNIQUE,
    "language"    TEXT NOT NULL,
    "code"    TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);
--Create voice TABLE
CREATE TABLE "voice" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL,
    "language"    TEXT NOT NULL,
    "gender"    TEXT NOT NULL,
    "type"    INTEGER NOT NULL,
    FOREIGN KEY("language") REFERENCES "language"("id"),
    PRIMARY KEY("id" AUTOINCREMENT)
);
-- Insert Languages
INSERT INTO "language" ("id", "language", "code")
VALUES ('am', 'English US', 'en-US');
INSERT INTO "language" ("id", "language", "code")
VALUES ('ar', 'Arabic', 'ar-XA');
INSERT INTO "language" ("id", "language", "code")
VALUES ('br', 'English UK', 'en-GB');
INSERT INTO "language" ("id", "language", "code")
VALUES ('cs', 'Czech (Czech Republic)', 'cs-CZ');
INSERT INTO "language" ("id", "language", "code")
VALUES ('cy', 'Welsh (United Kingdom)', 'cy-GB');
INSERT INTO "language" ("id", "language", "code")
VALUES ('da', 'Danish (Denmark)', 'da-DK');
INSERT INTO "language" ("id", "language", "code")
VALUES ('de', 'German (Germany)', 'de-DE');
INSERT INTO "language" ("id", "language", "code")
VALUES ('el', 'Greek (Greece)', 'el-GR');
INSERT INTO "language" ("id", "language", "code")
VALUES ('es', 'Spanish (Spain)', 'es-ES');
INSERT INTO "language" ("id", "language", "code")
VALUES ('fi', 'Finnish (Finland)', 'fi-FI');
INSERT INTO "language" ("id", "language", "code")
VALUES ('fr', 'French', 'fr-FR');
INSERT INTO "language" ("id", "language", "code")
VALUES ('hi', 'Hindi (India)', 'hi-IN');
INSERT INTO "language" ("id", "language", "code")
VALUES ('hu', 'Hungarian (Hungary)', 'hu-HU');
INSERT INTO "language" ("id", "language", "code")
VALUES ('id', 'Indonesian (Indonesia)', 'id-ID');
INSERT INTO "language" ("id", "language", "code")
VALUES ('is', 'Icelandic (Iceland)', 'is-IS');
INSERT INTO "language" ("id", "language", "code")
VALUES ('it', 'Italian (Italy)', 'it-IT');
INSERT INTO "language" ("id", "language", "code")
VALUES ('ja', 'Japanese', 'ja-JP');
INSERT INTO "language" ("id", "language", "code")
VALUES ('ko', 'Korean (Korea)', 'ko-KR');
INSERT INTO "language" ("id", "language", "code")
VALUES ('nl', 'Dutch (Netherlands)', 'nl-NL');
INSERT INTO "language" ("id", "language", "code")
VALUES ('no', 'Norwegian (Norway)', 'nb-NO');
INSERT INTO "language" ("id", "language", "code")
VALUES ('pl', 'Polish (Poland)', 'pl-PL');
INSERT INTO "language" ("id", "language", "code")
VALUES ('pt', 'Portuguese (Portugal)', 'pt-PT');
INSERT INTO "language" ("id", "language", "code")
VALUES ('pt-br', 'Portuguese (Brazil)', 'pt-BR');
INSERT INTO "language" ("id", "language", "code")
VALUES ('ro', 'Romanian', 'ro-RO');
INSERT INTO "language" ("id", "language", "code")
VALUES ('ru', 'Russian (Russia)', 'ru-RU');
INSERT INTO "language" ("id", "language", "code")
VALUES ('sk', 'Slovak (Slovakia)', 'sk-SK');
INSERT INTO "language" ("id", "language", "code")
VALUES ('sv', 'Swedish (Sweden)', 'sv-SE');
INSERT INTO "language" ("id", "language", "code")
VALUES ('tr', 'Turkish (Turkey)', 'tr-TR');
INSERT INTO "language" ("id", "language", "code")
VALUES ('uk', 'Ukrainian (Ukraine)', 'uk-UA');
INSERT INTO "language" ("id", "language", "code")
VALUES ('vi', 'Vietnamese', 'vi-VN');
INSERT INTO "language" ("id", "language", "code")
VALUES ('zh-cn', 'Chinese (S)', 'cmn-CN');
INSERT INTO "language" ("id", "language", "code")
VALUES ('zh-tw', 'Chinese (T)', 'zh-TW');

-- Insert voices
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Joey', 'am', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Justin', 'am', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Matthew', 'am', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Salli', 'am', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Joanna', 'am', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Ivy', 'am', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Amy', 'br', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Brian', 'br', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Emma', 'br', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('cs-CZ-Standard-A', 'cs', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Naja', 'da', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('da-DK-Standard-A', 'da', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Hans', 'de', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Vicki', 'de', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('German', 'de', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('el-GR-Standard-A', 'el', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Enrique', 'es', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Lucia', 'es', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Conchita', 'es', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('fi-FI-Standard-A', 'fi', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Mathieu', 'fr', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Lea', 'fr', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Celine', 'fr', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('hi-IN-Standard-A', 'hi', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('hi-IN-Standard-B', 'hi', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('hi-IN-Standard-C', 'hi', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('hu-HU-Standard-A', 'hu', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('id-ID-Standard-A', 'id', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('id-ID-Standard-B', 'id', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('id-ID-Standard-C', 'id', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Dora', 'is', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Karl', 'is', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Giorgio', 'it', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Bianca', 'it', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Carla', 'it', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Takumi', 'ja', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Mizuki', 'ja', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Seoyeon', 'ko', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('ko-KR-Standard-C', 'ko', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Lotte', 'nl', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Ruben', 'nl', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Liv', 'no', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('ko-KR-Standard-D', 'no', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Jacek', 'pl', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Jan', 'pl', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Ewa', 'pl', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Maja', 'pl', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Cristiano', 'pt', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Ines', 'pt', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Ricardo', 'pt-br', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Victoria', 'pt-br', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Camila', 'pt-br', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Carmen', 'ro', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Tatyana', 'ru', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Maxim', 'ru', 'Male', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('sk-SK-Standard-A', 'sk', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Astrid', 'sv', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('tr-TR-Standard-B', 'tr', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Filiz', 'tr', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('uk-UA-Standard-A', 'uk', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('vi-VN-Standard-A', 'vi', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('vi-VN-Standard-B', 'vi', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('vi-VN-Standard-C', 'vi', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('vi-VN-Standard-D', 'vi', 'Male', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('Zhiyu', 'zh-cn', 'Female', '1');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('zh-CN-Standard-A', 'zh-cn', 'Female', '0');
INSERT INTO "voice" ("name", "language", "gender", "type")
VALUES ('zh-TW-Standard-A', 'zh-tw', 'Female', '0');
"""

GET_VOICES_BY_LANGUAGE = """
SELECT name, code, gender, type
FROM language JOIN voice ON (language.id=voice.language)
WHERE language.id = ?;
"""

INLINE_OPTION = "    {index}. {voice} - {gender} - {type}"
