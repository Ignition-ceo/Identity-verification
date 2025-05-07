import builtins
from interfaces import IVpcRivStack
from infra.userportal.gateway.topology import RivUserPortalGateway
from infra.frontend.cognito.topology import RivCognitoForLivenes
from constructs import Construct
import aws_cdk as core
from aws_cdk import SecretValue
from aws_cdk import (
    CfnOutput,
    custom_resources as cr,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_amplify_alpha as amplify2,
)

class RivFrontEnd(Construct):
    '''
    Represents the root construct to create an Amplify App from GitHub
    '''
    def __init__(
        self,
        scope: Construct,
        id: str,
        riv_stack: IVpcRivStack,
        apigateway: RivUserPortalGateway,
        cognito: RivCognitoForLivenes
    ) -> None:
        super().__init__(scope, id)

        # Configure GitHub as the source for Amplify with personal repository
        github_provider = amplify2.GitHubSourceCodeProvider(
            self,
            'GitHubProvider',
            owner='Ignition-ceo',  # your GitHub user or organization
            repository='Identity-verification',  # your repository name
            oauth_token=SecretValue.ssm_secure(
                parameter_name='/rekognition-identity-verification/github-token'
            )
        )

        # Define the Amplify App
        self.amplify = amplify2.App(
            self,
            'RIV-Web-App',
            app_name=riv_stack.stack_name,
            source_code_provider=github_provider,
            auto_branch_creation=amplify2.AutoBranchCreation(
                auto_build=True,
                patterns=["main/*", "prod/*"],
            ),
            custom_rules=[
                amplify2.CustomRule(
                    source=r"</^((?!\.(css|gif|ico|jpg|js|png|txt|svg|woff|ttf)$).)*$/>",
                    target="/index.html",
                    status=amplify2.RedirectStatus.REWRITE,
                )
            ],
        )

        # Add environment variables to Amplify
        self.amplify.add_environment(
            name="REACT_APP_ENV_API_URL",
            value=apigateway.rest_api_url(),
        )
        self.amplify.add_environment(
            name="REACT_APP_IDENTITYPOOL_ID",
            value=cognito.idp.ref,
        )
        self.amplify.add_environment(
            name="REACT_APP_USERPOOL_ID",
            value=cognito.cognito.user_pool_id,
        )
        self.amplify.add_environment(
            name="REACT_APP_WEBCLIENT_ID",
            value=cognito.client.user_pool_client_id,
        )
        self.amplify.add_environment(
            name="REACT_APP_REGION",
            value=core.Stack.of(self).region,
        )

        # Create and configure the main branch
        main_branch = self.amplify.add_branch(
            'main',
            auto_build=True,
            branch_name='main'
        )

        # Output the Amplify app URL
        CfnOutput(
            self,
            'RIV-Web-App-URL',
            value=main_branch.branch_url,
            export_name='RIV-Web-App-URL',
        )
