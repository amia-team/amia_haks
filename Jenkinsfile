pipeline {
    agent any

    environment {
        CHANGES = 'false'
    }
    
    stages {
        stage('Check for changes'){
            when{
                not{
                    changeset "src/**/**/**"
                }
                expression{
                    return params.BUILD_ALL == 'No'
                }
            }
            steps{
                echo "Nothing to do."
            }
        }
        stage('Pack Amia Top') {
            when {
                changeset "src/hak/amia_top/**/**"
            }
            steps {
                echo 'Packing Amia top'
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_top"
                }
            }
        }
        stage('Pack Amia Parts') {
            when {
                changeset "src/hak/amia_parts/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_parts"
                }
            }
        }
        stage('Pack Amia Races') {
            when {
                changeset "src/hak/amia_races/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_races"
                }
            }
        }
        stage('Pack Amia amia_plc') {
            when {
                changeset "src/hak/amia_plc/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_plc"
                }
            }
        }
        stage('Pack Amia Items') {
            when {
                changeset "src/hak/amia_items/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_items"
                }
            }
        }
        stage('Pack Amia Rest') {
            when {
                changeset "src/hak/amia_rest/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_rest"
                }
            }
        }
        stage('Pack Amia A') {
            when {
                changeset "src/hak/amia_a/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_a"
                }
            }
        }
        stage('Pack Amia B') {
            when {
                changeset "src/hak/amia_b/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_b"
                }
            }
        }
        stage('Pack Amia C') {
            when {
                changeset "src/hak/amia_c/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_c"
                }
            }
        }
        stage('Pack Amia D') {
            when {
                changeset "src/hak/amia_robe/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_d"
                }
            }
        }
        stage('Pack Amia Music') {
            when {
                changeset "src/hak/amia_music/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_music"
                }
            }
        }
        stage('Pack Amia Override') {
            when {
                changeset "src/hak/amia_override/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_override"
                }
            }
        }
        stage('Pack Amia Override 2') {
            when {
                changeset "src/hak/amia_override2/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_override2"
                }
            }
        }
        stage('Pack Amia Creature') {
            when {
                changeset "src/hak/amia_creature/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_creature"
                }
            }
        }
		stage('Pack Amia Creature 2') {
            when {
                changeset "src/hak/amia_creature2/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_creature2"
                }
            }
        }
        stage('Pack Amia Skybox') {
            when {
                changeset "src/hak/amia_skybox/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_skybox"
                }
            }
        }
        stage('Pack Amia Weapons') {
            when {
                changeset "src/hak/amia_weapons/**/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_weapons"
                }
            }
        }
        stage('Pack Amia TLK') {
            when {
                changeset "src/tlk/amia_tlk/tlk/**"
            }
            steps {
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh tlk tlk"
                }
            }
        }
        stage('Pack everything') {
            when {
                expression {
                    return params.BUILD_ALL == 'Yes'
                }
            }
            steps {
 				script{
					sh "chmod +x linux-pack-all.sh"
					sh "dos2unix linux-pack-all.sh"
					sh "./linux-pack-all.sh"
				}
			}
        }
		stage('Deploy-Haks') {
            steps {
 				 script {
                    sh "chmod +x deploy.sh"
                    sh "dos2unix deploy.sh"
					sh "./linux-pack-all.sh"
                    sh "./deploy.sh /home/amia/amia_server/server/"
					sh "./deploy.sh /home/amia/amia_server/test_server/"
					sh "chmod +x cleanup.sh"
                    sh "dos2unix cleanup.sh"
					sh "./cleanup.sh"
                }
			}
        }
    }
    post {
        always {
            echo 'Finalizing results.' 
        }
        success {
            archiveArtifacts artifacts: '*.hak', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.tlk', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.zip', followSymlinks: false, allowEmptyArchive: true
            echo 'Build complete'
        }
    }
}