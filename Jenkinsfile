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
        stage('Before all'){
            steps{
                discordSend description: "Build for Amia content kicked off", footer: "Build start", link: env.BUILD_URL, title: "Build Kickoff", webhookURL: params.WEBHOOK
            }
        }
        stage('Pack Amia Top') {
            when {
                changeset "src/hak/amia_top/**/**"
            }
            steps {
                discordSend description: "Packing Amia Top", footer: "Amia top hak", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Parts", footer: "Amia parts", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Races", footer: "Amia races", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia PLC", footer: "Amia plc", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Items", footer: "Amia items", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Rest", footer: "Amia rest", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia A", footer: "Amia a", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia B", footer: "Amia b", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia C", footer: "Amia c", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia D", footer: "Amia d", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Music", footer: "Amia music", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing Amia Override", footer: "Amia override", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_override"
                }
            }
        }
        stage('Pack Amia Creature') {
            when {
                changeset "src/hak/amia_creature/**/**"
            }
            steps {
                discordSend description: "Packing Amia Creature", footer: "Amia creature", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_creature"
                }
            }
        }
        stage('Pack Amia Skybox') {
            when {
                changeset "src/hak/amia_skybox/**/**"
            }
            steps {
                discordSend description: "Packing Amia Skybox", footer: "Amia skybox", link: env.BUILD_URL, title: "Packaging Hak", webhookURL: params.WEBHOOK
                 script {
                    sh "chmod +x pack.sh"
                    sh "dos2unix pack.sh"
                    sh "./pack.sh hak amia_skybox"
                }
            }
        }
        stage('Pack Amia TLK') {
            when {
                changeset "src/tlk/amia_tlk/tlk/**"
            }
            steps {
                discordSend description: "Packing Amia TLK", footer: "Amia tlk", link: env.BUILD_URL, title: "Packaging TLK", webhookURL: params.WEBHOOK
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
                discordSend description: "Packing everything", footer: "Packing everything", link: env.BUILD_URL, title: "Packaging All Content", webhookURL: params.WEBHOOK
				script{
					sh "chmod +x linux-pack-all.sh"
					sh "dos2unix linux-pack-all.sh"
					sh "./linux-pack-all.sh"
				}
			}
        }
		stage('Deploy-Test') {
            when {
                expression {
                    return params.DEPLOY_ALL == 'Yes'
                }
				expression {
                    return params.ENVIRONMENT == 'Test'
                }
            }
            steps {
                discordSend description: "Deploying everything to Test", footer: "Deploying everything to Test", link: env.BUILD_URL, title: "Deploying All Content to Test", webhookURL: params.WEBHOOK
				 script {
                    sh "chmod +x deploy.sh"
                    sh "dos2unix deploy.sh"
                    sh "./deploy.sh /home/amia/amia_server/test_server/"
                }
			}
        }-
		stage('Deploy-Live') {
            when {
                expression {
                    return params.DEPLOY_ALL == 'Yes'
                }
				expression {
                    return params.ENVIRONMENT == 'Live'
                }
            }
            steps {
                discordSend description: "Deploying everything Live", footer: "Deploying everything Live", link: env.BUILD_URL, title: "Deploying All Content Live", webhookURL: params.WEBHOOK
				 script {
                    sh "chmod +x deploy.sh"
                    sh "dos2unix deploy.sh"
                    sh "./deploy.sh /home/amia/amia_server/server/"
                }
			}
        }
    }
    post {
        always {
            echo 'Finalizing results.' 
        }
        success {
            discordSend description: "", footer: "Successful build results for Amia content", link: env.BUILD_URL, result: currentBuild.currentResult, title: "Build Complete", webhookURL: params.WEBHOOK
            archiveArtifacts artifacts: '*.hak', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.tlk', followSymlinks: false, allowEmptyArchive: true
            archiveArtifacts artifacts: '*.zip', followSymlinks: false, allowEmptyArchive: true
            echo 'Build complete'
        }
    }
}